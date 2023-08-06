#  MIPLearn: Extensible Framework for Learning-Enhanced Mixed-Integer Optimization
#  Copyright (C) 2020-2022, UChicago Argonne, LLC. All rights reserved.
#  Released under the modified BSD license. See COPYING.md for more details.

from os.path import exists

from config import challenges, n_jobs
from miplearn.io import write_pkl_gz

if __name__ == "__main__":
    for challenge in challenges:
        if exists(f"data/{challenge.name}/"):
            print(f"Skipping data/{challenge.name}")
            continue
        print(f"\n{challenge.name}")
        data = challenge.generator.generate(challenge.n_samples)
        write_pkl_gz(
            data,
            f"data/{challenge.name}/",
            prefix=f"{challenge.name}-",
            n_jobs=n_jobs,
        )
