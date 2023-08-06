import pytest
import numpy as np
from numpy.testing import assert_allclose

from skcyto.flowsom import FlowSOM, get_group_means, get_group_cv
from skcyto.consensuscluster import ConsensusCluster
from minisom import MiniSom
from sklearn.datasets import make_blobs

@pytest.fixture
def test_data():
    X, _ = make_blobs(100, 5, centers = 2, random_state=42)
    return X

def test_get_group_means():
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    labels = np.array([0, 0, 1, 1])
    expected_output = {0: np.array([2, 3]), 1: np.array([6, 7])}

    result = get_group_means(X, labels)

    assert isinstance(result, dict)
    assert set(result.keys()) == set(expected_output.keys())
    for key in expected_output.keys():
        assert_allclose(result[key], expected_output[key])

def test_get_group_cv():
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    labels = np.array([0, 0, 1, 1])
    expected_output = {0: np.array([0.5, 0.33333333]), 1: np.array([0.16666667, 0.14285714])}
    
    result = get_group_cv(X, labels)

    assert isinstance(result, dict)    
    assert set(result.keys()) == set(expected_output.keys())
    for key in expected_output.keys():
        assert_allclose(result[key], expected_output[key])

def test_calc_within_cluster_sum_squared_error():
    fsom = FlowSOM()
    random_state = np.random.RandomState(42)
    X = random_state.randn(10000, 5)
    for i in range (1, 6):
        y = random_state.choice(i, 10000)
        wss = fsom._calc_within_cluster_sum_squared_error(X, y)
        # We draw from standardnormal distribution, expect a variance of 1 per feature (which we have 5)
        # For each cluster we add, we expect to have another variance of 1.
        # Therefore we expect to have approximately a wss of 5 * number of clusters
        assert_allclose(wss, 5*i, rtol = 0.05)

def test_find_elbow():
    y = np.array([0, 1, 2, 1.5, 1, 0.5]).reshape(-1, 1) # Peak at position 2
    X = np.arange(len(y)).reshape(-1, 1)
    fsom = FlowSOM()
    elbow = fsom._find_elbow(X, y)
    assert elbow == 2

def test_smooth():
    x = np.array([0., 1., 2., 1., 0.])
    fsom = FlowSOM()
    assert_allclose(fsom._smooth(x), np.array([0., 1., 1.8, 1., 0.]))

def test_FlowSOM(test_data):
    fsom = FlowSOM()
    # Attributes during init
    expected_attributes = ["nodes_x", "nodes_y", "sigma", "learning_rate", "n_iter", 
                           "neighborhood_function", "activation_distance",
                           "random_state", "k_min", "k_max"]
    
    for attr in expected_attributes:
        assert hasattr(fsom, attr)

    assert fsom.nodes_x == 10
    assert fsom.nodes_y == 10
    assert fsom.sigma == 1
    assert fsom.learning_rate == 0.5
    assert fsom.n_iter == 10
    assert fsom.neighborhood_function == "gaussian"
    assert fsom.activation_distance == "euclidean"
    assert fsom.random_state is None
    assert fsom.k_min is None
    assert fsom.k_max == 20

    # Attributes during fit
    fsom.fit(test_data)

    expected_attributes = ["importance_", "X_", "n_nodes_",
                            "som_", "som_weights_", "som_labels_",
                            "mst_", 
                            "n_clusters_", "som_metacluster_labels_", "consensus_clustering_", "labels_"]
    for attr in expected_attributes:
        assert hasattr(fsom, attr)

    assert type(fsom.X_) is np.ndarray
    assert type(fsom.n_nodes_) is int
    assert fsom.n_nodes_ == 100
    assert type(fsom.som_) is MiniSom
    assert type(fsom.som_weights_) is np.ndarray
    assert fsom.som_weights_.shape == (100, 5)
    assert type(fsom.som_labels_) is np.ndarray
    assert fsom.som_labels_.shape == (100,)
    assert type(fsom.consensus_clustering_) is ConsensusCluster
    assert type(fsom.n_clusters_) is int
    assert type(fsom.som_metacluster_labels_) is np.ndarray
    assert fsom.som_metacluster_labels_.shape == (100,)
    assert type(fsom.labels_) is np.ndarray
    assert fsom.labels_.shape == (100,)

    