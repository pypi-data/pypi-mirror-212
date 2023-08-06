#  MIPLearn: Extensible Framework for Learning-Enhanced Mixed-Integer Optimization
#  Copyright (C) 2020-2022, UChicago Argonne, LLC. All rights reserved.
#  Released under the modified BSD license. See COPYING.md for more details.

import random
from dataclasses import dataclass
from typing import Any, Callable, List

import numpy as np
from scipy.stats import randint, uniform
from sklearn.decomposition import PCA
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.tree import DecisionTreeClassifier

from miplearn.classifiers.minprob import MinProbabilityClassifier
from miplearn.classifiers.singleclass import SingleClassFix
from miplearn.collectors.basic import BasicCollector
from miplearn.components.primal.actions import (
    SetWarmStart,
    FixVariables,
    EnforceProximity,
)
from miplearn.components.primal.expert import ExpertPrimalComponent
from miplearn.components.primal.indep import IndependentVarsPrimalComponent
from miplearn.components.primal.joint import JointVarsPrimalComponent
from miplearn.components.primal.mem import (
    MemorizingPrimalComponent,
    SelectTopSolutions,
    MergeTopSolutions,
)
from miplearn.extractors.fields import H5FieldsExtractor
from miplearn.problems.binpack import BinPackGenerator, build_binpack_model
from miplearn.problems.multiknapsack import (
    MultiKnapsackGenerator,
    build_multiknapsack_model,
)
from miplearn.problems.pmedian import PMedianGenerator, build_pmedian_model
from miplearn.problems.setcover import SetCoverGenerator, build_setcover_model_gurobipy
from miplearn.problems.setpack import SetPackGenerator, build_setpack_model
from miplearn.problems.stab import (
    MaxWeightStableSetGenerator,
    build_stab_model_gurobipy,
    build_stab_model_pyomo,
)
from miplearn.problems.tsp import TravelingSalesmanGenerator, build_tsp_model
from miplearn.problems.uc import UnitCommitmentGenerator, build_uc_model
from miplearn.problems.vertexcover import (
    MinWeightVertexCoverGenerator,
    build_vertexcover_model,
)

dev = True

n_jobs = 8 if dev else 32
timelimit_collect = 900
timelimit_benchmark = 300
n_seeds = 1 if dev else 5

random.seed(42)
np.random.seed(42)


@dataclass
class Challenge:
    name: str
    generator: Any
    build_model: Callable
    n_samples: int = 16 if dev else 1056
    n_train: int = 0 if dev else 1024


@dataclass
class Method:
    name: str
    components: List


# CHALLENGES
# -----------------------------------------------------------------------------

challenges: List[Challenge] = []

# # Bin Packing
# for i in [] if dev else range(5, 10):
#     n = i * 100
#     challenges.append(
#         Challenge(
#             name=f"binpack-n{n:03d}",
#             generator=BinPackGenerator(
#                 n=randint(low=n, high=n + 1),
#                 sizes=uniform(loc=0, scale=25),
#                 capacity=uniform(loc=100, scale=0),
#                 sizes_jitter=uniform(loc=0.9, scale=0.2),
#                 capacity_jitter=uniform(loc=0.9, scale=0.2),
#                 fix_items=True,
#             ),
#             build_model=build_binpack_model,
#         )
#     )
#
# # Multi-knapsack
# for i in [3] if dev else range(5, 10):
#     n = 25 * i
#     m = i
#     challenges.append(
#         Challenge(
#             name=f"multiknapsack-n{n:03d}-m{m}",
#             generator=MultiKnapsackGenerator(
#                 n=randint(low=n, high=n + 1),
#                 m=randint(low=m, high=m + 1),
#                 w=uniform(loc=0, scale=1000),
#                 K=uniform(loc=100, scale=0),
#                 u=uniform(loc=1, scale=0),
#                 alpha=uniform(loc=0.25, scale=0),
#                 w_jitter=uniform(loc=0.95, scale=0.1),
#                 p_jitter=uniform(loc=0.75, scale=0.5),
#                 fix_w=True,
#             ),
#             build_model=build_multiknapsack_model,
#         )
#     )
#
# # Capacitated p-median
# for i in [] if dev else range(5, 10):
#     n = 50 * i
#     p = i
#     challenges.append(
#         Challenge(
#             name=f"pmedian-n{n:03d}-p{p:01d}",
#             generator=PMedianGenerator(
#                 x=uniform(loc=0.0, scale=100.0),
#                 y=uniform(loc=0.0, scale=100.0),
#                 n=randint(low=n, high=n + 1),
#                 p=randint(low=p, high=p + 1),
#                 demands=uniform(loc=0, scale=10),
#                 capacities=uniform(loc=0, scale=250),
#                 distances_jitter=uniform(loc=0.9, scale=0.2),
#                 demands_jitter=uniform(loc=0.9, scale=0.2),
#                 capacities_jitter=uniform(loc=0.9, scale=0.2),
#                 fixed=True,
#             ),
#             build_model=build_pmedian_model,
#         )
#     )
#
# # Set Cover
# for i in [7] if dev else range(9, 14):
#     n = 250 * i
#     m = 10 * i
#     challenges.append(
#         Challenge(
#             name=f"setcover-n{n:04d}-m{m:03d}",
#             generator=SetCoverGenerator(
#                 n_elements=randint(low=m, high=m + 1),
#                 n_sets=randint(low=n, high=n + 1),
#                 costs=uniform(loc=0.0, scale=1000.0),
#                 costs_jitter=uniform(loc=0.90, scale=0.20),
#                 density=uniform(loc=0.05, scale=0.00),
#                 K=uniform(loc=25.0, scale=0.0),
#                 fix_sets=True,
#             ),
#             build_model=build_setcover_model_gurobipy,
#         )
#     )
#
# # Set Pack
# for i in [12] if dev else range(14, 19):
#     n = 100 * i
#     m = 10 * i
#     challenges.append(
#         Challenge(
#             name=f"setpack-n{n:04d}-m{m:03d}",
#             generator=SetPackGenerator(
#                 n_elements=randint(low=m, high=m + 1),
#                 n_sets=randint(low=n, high=n + 1),
#                 costs=uniform(loc=0.0, scale=1000.0),
#                 costs_jitter=uniform(loc=0.75, scale=0.5),
#                 density=uniform(loc=0.10, scale=0.00),
#                 K=uniform(loc=10.0, scale=0.0),
#                 fix_sets=True,
#             ),
#             build_model=build_setpack_model,
#         )
#     )

# Maximum Weight Stable Set
for i in [16] if dev else range(18, 23):
    n = 10 * i
    challenges.append(
        Challenge(
            name=f"stab-n{n:03d}",
            generator=MaxWeightStableSetGenerator(
                w=uniform(loc=100.0, scale=25.0),
                n=randint(low=n, high=n + 1),
                p=uniform(loc=0.05, scale=0.0),
                fix_graph=True,
            ),
            build_model=build_stab_model_pyomo,
        )
    )

# # Traveling Salesman
# for i in [] if dev else range(7, 12):
#     n = i * 50
#     challenges.append(
#         Challenge(
#             name=f"tsp-n{n:03d}",
#             generator=TravelingSalesmanGenerator(
#                 n=randint(low=n, high=n + 1),
#                 x=uniform(loc=0.0, scale=1000.0),
#                 y=uniform(loc=0.0, scale=1000.0),
#                 gamma=uniform(loc=0.90, scale=0.20),
#                 fix_cities=True,
#                 round=True,
#             ),
#             build_model=build_tsp_model,
#         )
#     )

# # Unit Commitment
# for i in [] if dev else range(6, 11):
#     g = 250 * i
#     t = i * 4
#     challenges.append(
#         Challenge(
#             name=f"uc-g{g:04d}-t{t:02d}",
#             generator=UnitCommitmentGenerator(
#                 n_units=randint(low=g, high=g + 1),
#                 n_periods=randint(low=t, high=t + 1),
#                 max_power=uniform(loc=50, scale=450),
#                 min_power=uniform(loc=0.5, scale=0.25),
#                 cost_startup=uniform(loc=0, scale=10_000),
#                 cost_prod=uniform(loc=0, scale=50),
#                 cost_fixed=uniform(loc=0, scale=1_000),
#                 min_uptime=randint(low=2, high=8),
#                 min_downtime=randint(low=2, high=8),
#                 cost_jitter=uniform(loc=0.75, scale=0.5),
#                 demand_jitter=uniform(loc=0.9, scale=0.2),
#                 fix_units=True,
#             ),
#             build_model=build_uc_model,
#         )
#     )

# # Vertex Cover
# for i in [] if dev else range(16, 21):
#     n = 10 * i
#     challenges.append(
#         Challenge(
#             name=f"vertexcover-n{n:03d}",
#             generator=MinWeightVertexCoverGenerator(
#                 w=uniform(loc=100.0, scale=25.0),
#                 n=randint(low=n, high=n + 1),
#                 p=uniform(loc=0.25, scale=0),
#                 fix_graph=True,
#             ),
#             build_model=build_vertexcover_model,
#         )
#     )

# COLLECTORS
# -----------------------------------------------------------------------------
collectors = [
    BasicCollector(),
    # BranchPriorityCollector(
    #     time_limit=timelimit_collect,
    #     node_limit=500,
    # ),
    # LazyCollector(
    #     time_limit=timelimit_collect,
    #     min_constrs=100_000,
    # ),
]

# METHODS
# -----------------------------------------------------------------------------

# baseline & experts
methods: List[Method] = [
    Method(
        name="baseline",
        components=[],
    ),
    Method(
        name="ws:exp",
        components=[
            ExpertPrimalComponent(action=SetWarmStart()),
        ],
    ),
    Method(
        name="fix:exp",
        components=[
            ExpertPrimalComponent(action=FixVariables()),
        ],
    ),
    Method(
        name="prox:exp",
        components=[
            ExpertPrimalComponent(action=EnforceProximity(0.01)),
        ],
    ),
]

# extractor = H5FieldsExtractor(
#     instance_fields=[
#         "lp_obj_value",
#         "lp_var_values",
#         "lp_var_reduced_costs",
#         "lp_constr_dual_values",
#         "static_var_obj_coeffs",
#         "static_constr_rhs",
#     ],
#     var_fields=["lp_var_features"],
# )
#
# for k in [25]:
#     methods.append(
#         Method(
#             name=f"ws:collect:{k}",
#             components=[
#                 MemorizingPrimalComponent(
#                     clf=DecisionTreeClassifier(),
#                     constructor=SelectTopSolutions(k),
#                     extractor=extractor,
#                     action=SetWarmStart(),
#                 ),
#             ],
#         )
#     )
#     methods.append(
#         Method(
#             name=f"ws:merge:{k}",
#             components=[
#                 MemorizingPrimalComponent(
#                     clf=DecisionTreeClassifier(),
#                     constructor=MergeTopSolutions(k, thresholds=[0.05, 0.95]),
#                     extractor=extractor,
#                     action=SetWarmStart(),
#                 ),
#             ],
#         )
#     )
#     methods.append(
#         Method(
#             name=f"fix:merge:{k}",
#             components=[
#                 MemorizingPrimalComponent(
#                     clf=DecisionTreeClassifier(),
#                     constructor=MergeTopSolutions(k, thresholds=[0.05, 0.95]),
#                     extractor=extractor,
#                     action=FixVariables(),
#                 ),
#             ],
#         )
#     )
#
# for k1 in [25]:
#     for k2 in [1, 5, 10]:
#         methods.append(
#             Method(
#                 name=f"prox:merge:{k1}:{k2}",
#                 components=[
#                     MemorizingPrimalComponent(
#                         clf=DecisionTreeClassifier(),
#                         constructor=MergeTopSolutions(k1, thresholds=[0.05, 0.95]),
#                         extractor=extractor,
#                         action=EnforceProximity(k2 / 100),
#                     ),
#                 ],
#             )
#         )

# methods.append(
#     Method(
#         name=f"ws:j:tree",
#         components=[
#             JointVarsPrimalComponent(
#                 clf=DecisionTreeClassifier(),
#                 extractor=extractor,
#             ),
#         ],
#     )
# )
#
# methods.append(
#     Method(
#         name=f"ws:i:tree",
#         components=[
#             IndependentVarsPrimalComponent(
#                 base_clf=SingleClassFix(
#                     MinProbabilityClassifier(
#                         LogisticRegression(),
#                         thresholds=[0.99, 0.99],
#                     )
#                 ),
#                 extractor=extractor,
#             ),
#         ],
#     )
# )
