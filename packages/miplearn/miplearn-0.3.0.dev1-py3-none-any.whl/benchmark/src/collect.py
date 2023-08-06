#  MIPLearn: Extensible Framework for Learning-Enhanced Mixed-Integer Optimization
#  Copyright (C) 2020-2022, UChicago Argonne, LLC. All rights reserved.
#  Released under the modified BSD license. See COPYING.md for more details.
import logging
import random

from miplearn.parallel import p_umap

from config import challenges, n_jobs, collectors

logger = logging.getLogger()


def collect():
    def _collect(args):
        challenge_idx, sample_idx = args
        challenge = challenges[challenge_idx]
        data = f"data/{challenge.name}/{challenge.name}-{sample_idx:05d}.pkl.gz"
        try:
            for c in collectors:
                c.collect([data], challenge.build_model)
        except:
            logger.exception(f"Failed sample: {challenge.name} {sample_idx}")

    combinations = [
        (challenge_idx, sample_idx)
        for (challenge_idx, challenge) in enumerate(challenges)
        for sample_idx in range(challenge.n_samples)
    ]

    random.shuffle(combinations)

    if n_jobs > 1:
        p_umap(
            _collect,
            combinations,
            num_cpus=n_jobs,
            desc="collect",
            smoothing=0,
        )
    else:
        for args in combinations:
            _collect(args)


if __name__ == "__main__":
    collect()
