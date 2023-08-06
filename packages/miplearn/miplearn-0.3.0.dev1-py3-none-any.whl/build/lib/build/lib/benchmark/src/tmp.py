import logging
from miplearn.h5 import H5File
from glob import glob
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import logging
from tqdm.auto import tqdm
import sys
import warnings

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils import resample
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import cross_val_score
from sklearn.multioutput import MultiOutputClassifier, ClassifierChain
from scipy import sparse
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.multiclass import unique_labels


logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.DEBUG)
logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# stdout_handler = logging.StreamHandler(sys.stdout)
# stdout_handler.setLevel(logging.DEBUG)
# stdout_handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
# logger.addHandler(stdout_handler)


class ConditionalClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, parent_clf, threshold=[0.01, 0.99]):
        self.parent_clf = parent_clf
        self.threshold = threshold
        self.mean_ = None

    def fit(self, x, y):
        if self.threshold[0] < y.mean() < self.threshold[1]:
            self.parent_clf.fit(x, y)
            self.classes_ = self.parent_clf.classes_
        else:
            self.mean_ = y.mean()
            self.classes_ = unique_labels(y)

    def predict(self, x):
        if self.mean_ is not None:
            return np.full(x.shape[0], np.round(self.mean_))
        else:
            return self.parent_clf.predict(x)


def run(max_samples=1_000_000):
    logger.info("Reading training data...")
    X, y = [], []
    for h5_filename in tqdm(
        glob("benchmark/data/setcover-n2750-m110/*.h5"), desc="read"
    ):
        with H5File(h5_filename, "r") as h5:
            var_values = h5.get_array("mip_var_values")
            var_features = h5.get_array("lp_var_features")
            var_types = h5.get_array("static_var_types")
            assert var_values is not None
            assert var_features is not None
            assert var_types is not None

            bin_var_indices = np.where(var_types == b"B")[0]
            X.append(var_features[bin_var_indices, :])
            y.append(var_values[bin_var_indices])

    logger.info("Constructing matrices...")
    X = np.vstack(X)
    y = np.hstack(y)
    assert len(X.shape) == 2
    n_samples, n_features = X.shape
    assert y.shape == (n_samples,)
    logger.info(f"Dataset has {n_samples:,d} samples and {n_features:,d} features")

    if n_samples > max_samples:
        logger.info(f"Too many samples. Resampling...")
        X, y = resample(X, y, n_samples=max_samples)
        n_samples, n_features = X.shape
        logger.info(f"Dataset has {n_samples:,d} samples and {n_features:,d} features")

    candidates = {
        "Dummy": DummyClassifier(),
        "Logistic": make_pipeline(
            StandardScaler(),
            LogisticRegression(),
        ),
        "GradientBoost": GradientBoostingClassifier(
            n_estimators=25,
            min_samples_split=10,
            max_depth=5,
        ),
    }

    best_clf = None
    best_clf_name = None
    best_score = -float("inf")

    for (clf_name, clf) in candidates.items():
        logger.info(f"Evaluating {clf_name}...")
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=ConvergenceWarning)
            score = np.mean(cross_val_score(clf, X, y, cv=3))
        logger.info(f"    score = {score:.5f}")

        if score > best_score:
            best_score = score
            best_clf_name, best_clf = clf_name, clf

    logger.info(f"Selecting {best_clf_name}")


def run2():
    def _extract(h5_filename):
        with H5File(h5_filename, "r") as h5:
            var_types = h5.get_array("static_var_types")
            x = np.hstack(
                [
                    h5.get_array("static_var_obj_coeffs"),
                    h5.get_array("static_constr_rhs"),
                    h5.get_array("lp_var_values"),
                ]
            )
            y = h5.get_array("mip_var_values")
            bin_var_indices = np.where(var_types == b"B")[0]
            return x, y[bin_var_indices]

    logger.info("Reading training data...")
    x, y = [], []
    for h5_filename in tqdm(
        glob("benchmark/data/setcover-n2750-m110/*.h5"), desc="read"
    ):
        x_sample, y_sample = _extract(h5_filename)
        x.append(x_sample)
        y.append(y_sample)

    logger.info("Constructing matrices...")
    x = np.array(x)
    y = np.array(y)
    print(x.shape)
    print(y.shape)
    assert len(x.shape) == 2
    assert len(y.shape) == 2
    n_samples, n_features = x.shape
    logger.info(f"Dataset has {n_samples:,d} samples and {n_features:,d} features")

    # if n_samples > max_samples:
    #     logger.info(f"Too many samples. Resampling...")
    #     X, y = resample(X, y, n_samples=max_samples)
    #     n_samples, n_features = X.shape
    #     logger.info(f"Dataset has {n_samples:,d} samples and {n_features:,d} features")

    # clf = DecisionTreeClassifier(
    #     min_samples_split=10,
    #     max_depth=5,
    # )
    clf = ClassifierChain(
        ConditionalClassifier(
            make_pipeline(
                StandardScaler(),
                LogisticRegression(),
            ),
        ),
    )
    clf.fit(x, y)
    y_pred = clf.predict(x)
    print(len(y_pred))
    print(sparse.csr_matrix(y[0, :]))
    print()
    print(sparse.csr_matrix(y_pred[0, :]))


class VarObjCoeffExtractor:
    def extract(self, h5):
        var_obj_coeffs = h5.get_array("static_var_obj_coeffs")
        assert var_obj_coeffs is not None
        return var_obj_coeffs


class TopKSolutions:
    def __init__(self, k):
        self.k = k

    def construct(self, y_proba, solutions, var_names):
        assert len(y_proba.shape) == 1
        assert len(y_proba) == len(solutions)
        top_sol_indices = np.argpartition(y_proba, -self.k)[-self.k :]
        return [solutions[i] for i in top_sol_indices]


def run_3(
    extractor=VarObjCoeffExtractor(),
    constructor=TopKSolutions(3),
):
    h5_filenames = glob("benchmark/data/setcover-n2750-m110/*.h5")
    n_samples = len(h5_filenames)

    logger.info("Reading training data...")
    x, y, n_features = [], [], None
    solutions, bin_var_names = [], None
    solution_to_idx = {}
    for h5_filename in tqdm(h5_filenames, desc="read"):
        with H5File(h5_filename, "r") as h5:
            # Read optimal solution
            var_values = h5.get_array("mip_var_values")
            var_types = h5.get_array("static_var_types")
            assert var_values is not None
            assert var_types is not None

            # Extract binary part
            bin_var_indices = np.where(var_types == b"B")[0]
            bin_var_values = var_values[bin_var_indices]

            # Extract variable names
            if bin_var_names is None:
                var_names = h5.get_array("static_var_names")
                assert var_names is not None
                bin_var_names = var_names[bin_var_indices]

            # Store solution
            sol = tuple(np.where(bin_var_values)[0])
            if sol not in solution_to_idx:
                solutions.append(
                    {
                        var_name: bin_var_values[var_idx]
                        for (var_idx, var_name) in enumerate(bin_var_names)
                    }
                )
                solution_to_idx[sol] = len(solution_to_idx)
            y.append(solution_to_idx[sol])

            # Extract features
            x_sample = extractor.extract(h5)
            assert len(x_sample.shape) == 1
            if n_features is None:
                n_features = len(x_sample)
            else:
                assert len(x_sample) == n_features
            x.append(x_sample)

    logger.info("Constructing matrices...")
    x = np.vstack(x)
    y = np.array(y)
    assert len(x.shape) == 2
    assert x.shape[0] == n_samples
    assert x.shape[1] == n_features
    assert y.shape == (n_samples,)
    n_classes = len(solution_to_idx)
    logger.info(
        f"Dataset has {n_samples:,d} samples, {n_features:,d} features and {n_classes:,d} classes"
    )

    clf = DecisionTreeClassifier(max_depth=3)
    clf.fit(x, y)
    y_proba = clf.predict_proba(x)

    sols = constructor.construct(y_proba[0, :], solutions, var_names)


run_3()
