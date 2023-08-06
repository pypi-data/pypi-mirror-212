#  MIPLearn: Extensible Framework for Learning-Enhanced Mixed-Integer Optimization
#  Copyright (C) 2020-2022, UChicago Argonne, LLC. All rights reserved.
#  Released under the modified BSD license. See COPYING.md for more details.

import json
import logging
import os
import pickle
import random
import re
import sys
from contextlib import redirect_stdout
from distutils.dir_util import mkpath
from glob import glob
from io import StringIO
from os.path import dirname, exists
from pathlib import Path
from tempfile import NamedTemporaryFile
from time import time

import pandas as pd

from config import challenges, methods, n_jobs, n_seeds
from miplearn.h5 import H5File
from miplearn.io import _RedirectOutput
from miplearn.parallel import p_umap

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.ERROR)
stdout_handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
logger.addHandler(stdout_handler)

# -----------------------------------------------------------------------------


def fit():
    def _fit(args):
        # Parse arguments
        method_idx, challenge_idx = args
        method = methods[method_idx]
        challenge = challenges[challenge_idx]

        # Compute filenames
        pkl_filename = f"results/{challenge.name}/{method.name}/model.pkl"
        log_filename = pkl_filename.replace(".pkl", ".log")

        # Skip instances that have already been processed
        if exists(pkl_filename):
            return

        # Create folder
        mkpath(dirname(log_filename))

        # Set up logger
        file_handler = logging.FileHandler(log_filename, mode="w")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
        logger.addHandler(file_handler)

        # Fit
        data_filenames = sorted(glob(f"data/{challenge.name}/*.pkl.gz"))
        h5_filenames = [f"{filename}.h5" for filename in data_filenames]
        train_h5 = h5_filenames[: challenge.n_train]
        for c in method.components:
            c.fit(train_h5)

        # Pickle
        _write_pkl(method, pkl_filename)

        # Tear down logger
        logger.removeHandler(file_handler)

    initial_time = time()
    combinations = [
        (method_idx, challenge_idx)
        for method_idx in range(len(methods))
        for challenge_idx in range(len(challenges))
    ]
    random.shuffle(combinations)
    if n_jobs > 1:
        p_umap(
            _fit,
            combinations,
            num_cpus=n_jobs,
            desc="fit",
            smoothing=0,
        )
    else:
        [_fit(c) for c in combinations]

    elapsed_time = time() - initial_time
    print(f"total time: {elapsed_time:.2f} s")


# -----------------------------------------------------------------------------


def benchmark():
    def _benchmark(args):
        # Parse arguments
        challenge_idx, sample_idx, method_idx, mip_seed = args
        challenge = challenges[challenge_idx]
        method = methods[method_idx]

        # Compute filenames
        log_filename = f"results/{challenge.name}/{method.name}/{sample_idx:05d}-{mip_seed:05d}.log"
        stats_filename = log_filename.replace(".log", ".json")
        pkl_filename = f"results/{challenge.name}/{method.name}/model.pkl"
        data_filename = (
            f"data/{challenge.name}/{challenge.name}-{sample_idx:05d}.pkl.gz"
        )
        h5_filename = f"data/{challenge.name}/{challenge.name}-{sample_idx:05d}.h5"

        # Skip instances that have already been processed
        if exists(stats_filename):
            return

        # Create folder
        mkpath(dirname(log_filename))

        # Set up logger
        file_handler = logging.FileHandler(log_filename, mode="w")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
        logger.addHandler(file_handler)

        try:
            with NamedTemporaryFile() as tempfile:
                with H5File(tempfile.name) as h5:
                    components = _read_pkl(pkl_filename).components
                    with _RedirectOutput([]):
                        model = challenge.build_model(data_filename)
                    model.extract_after_load(h5)
                    stats = {}
                    for comp in components:
                        comp.before_mip(h5_filename, model, stats)
                    streams = [StringIO()]
                    with _RedirectOutput(streams):
                        model.optimize()
                    log = streams[0].getvalue()
                    model.extract_after_mip(h5)

                    var_types = h5.get_array("static_var_types")
                    constr_lhs = h5.get_sparse("static_constr_lhs")
                    n_vars = len(var_types)
                    n_int_vars = int((var_types == b"I").sum())
                    n_bin_vars = int((var_types == b"B").sum())
                    mip_val = h5.get_scalar("mip_obj_value")
                    mip_bound = h5.get_scalar("mip_obj_bound")
                    mip_gap = h5.get_scalar("mip_gap")
                    mip_time = h5.get_scalar("mip_wallclock_time")
                    mip_nodes = h5.get_scalar("mip_node_count")
                    (ws_value, ws_time), ws_gap = (
                        _extract_warm_start_stats(log),
                        None,
                    )
                    if ws_value is not None:
                        ws_gap = 100 * abs(ws_value - mip_bound) / abs(ws_value)
                    if "Heuristic" in stats:
                        mip_bound = None
                        mip_gap = None
                    stats.update(
                        {
                            "Challenge": challenge.name,
                            "Instance": f"{challenge.name}-{sample_idx:05d}",
                            "Method": method.name,
                            "MIP seed": mip_seed,
                            "Objective value": mip_val,
                            "Objective bound": mip_bound,
                            "Wallclock time (s)": mip_time,
                            "Node count": mip_nodes,
                            "Relative MIP gap (%)": mip_gap,
                            "Variables": n_vars,
                            "Integer variables": n_int_vars,
                            "Binary variables": n_bin_vars,
                            "Constraints": constr_lhs.shape[0],
                            "Non-zeros": constr_lhs.nnz,
                            "WS: Objective value": ws_value,
                            "WS: Processing time (s)": ws_time,
                            "WS: Relative MIP gap (%)": ws_gap,
                        }
                    )

                    # Write stats
                    _write_json(stats, stats_filename)
        except:
            logger.exception(f"Failed sample: {args}")

        # Tear down logging
        logger.removeHandler(file_handler)

    initial_time = time()
    combinations = [
        (challenge_idx, sample_idx, method_idx, mip_seed)
        for (challenge_idx, challenge) in enumerate(challenges)
        for sample_idx in range(challenge.n_train, challenge.n_samples)
        for mip_seed in [1000 + i for i in range(n_seeds)]
        for (method_idx, method) in enumerate(methods)
    ]
    random.shuffle(combinations)

    if n_jobs > 1:
        p_umap(
            _benchmark,
            combinations,
            num_cpus=n_jobs,
            desc="benchmark",
            smoothing=0,
        )
    else:
        [_benchmark(c) for c in combinations]

    elapsed_time = time() - initial_time
    print(f"total time: {elapsed_time:.2f} s")


# -----------------------------------------------------------------------------


def _write_csv(results, filename):
    Path(dirname(filename)).mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(results)
    df["Method"] = pd.Categorical(df["Method"], [m.name for m in methods])
    df.sort_values(by=["Challenge", "Instance", "Method", "MIP seed"], inplace=True)
    df.to_csv(filename, index=False)


def _write_json(obj, filename):
    with open(filename, "w") as f:
        json.dump(obj, f, indent=2)


def _write_pkl(obj, filename):
    with open(filename, "wb") as f:
        pickle.dump(obj, f)


def _read_pkl(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def _silence_stdout():
    return redirect_stdout(open(os.devnull, "w"))


def _extract_warm_start_stats(log):
    ws_value = None
    ws_time = None
    for line in log.splitlines():
        matches = re.findall("Loaded user MIP start .*with objective (.*)", line)
        if len(matches) > 0:
            ws_value = float(matches[0])

        matches = re.findall("Processed .*MIP starts? in (.*) seconds", line)
        if len(matches) > 0:
            ws_time = float(matches[0])

    return ws_value, ws_time


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    fit()
    benchmark()
