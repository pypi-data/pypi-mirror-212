import pytest

import numpy as np
from numpy.testing import assert_equal
from sklearn.datasets import make_blobs
from sklearn.cluster import AgglomerativeClustering
from skcyto import ConsensusCluster

@pytest.fixture
def test_data():
    X, _ = make_blobs(100, 5, centers = 2, random_state=42)
    return X

def test_k_handling(test_data):
    with pytest.raises(Exception):
        CClust = ConsensusCluster(
            k_max = 1,
            n_iter = 10
        ).fit(test_data)
    
    with pytest.raises(Exception):
        CClust = ConsensusCluster(
            k_min = 2,
            k_max = 1,
            n_iter = 10
        ).fit(test_data)

    with pytest.warns(UserWarning):
        CClust = ConsensusCluster(
            k_min = 1,
            n_iter = 10
        ).fit(test_data)

@pytest.mark.filterwarnings("ignore::UserWarning") # Ignore the warning rasied when k_min is set to 1
def test_construct_k_candidates():
    CClust = ConsensusCluster(k_max = 2)
    assert CClust._construct_k_candidates() == np.array([2])
    CClust = ConsensusCluster(k_max = 5)
    assert CClust._construct_k_candidates() == np.array([5])

    CClust = ConsensusCluster(k_min = 2, k_max = 5)
    assert_equal(CClust._construct_k_candidates(), np.arange(2, 6))

    CClust = ConsensusCluster(k_min = 1, k_max = 5)
    assert_equal(CClust._construct_k_candidates(), np.arange(2, 6))

def test_update_connectivity_matrix():
    num_instances = 5
    instance_ids = np.arange(num_instances) # Assume no subsampling for easier testing
    labels = np.array([0, 0, 0, 1, 1])

    connectivity_matrix = np.zeros(shape = (num_instances, num_instances))
    
    CClust = ConsensusCluster()
    connectivity_matrix = CClust._update_connectivity_matrix(connectivity_matrix, instance_ids, labels)

    connectivity_matrix_expected = np.array([
        [0., 1., 1., 0., 0.],
        [1., 0., 1., 0., 0.],
        [1., 1., 0., 0., 0.],
        [0., 0., 0., 0., 1.],
        [0., 0., 0., 1., 0.]
    ])
    assert_equal(connectivity_matrix, connectivity_matrix_expected)


def test_determine_best_k(test_data):
    CClust = ConsensusCluster(k_min = 2, k_max = 4, n_iter = 10)
    CClust.fit(test_data)
    assert CClust.k_best_ >= 2
    assert CClust.k_best_ <= 4


@pytest.mark.skip(reason = "Consensus clustering does not always return correct k. FlowSom does not rely on CClust to find it.")
def test_that_correct_k_is_found_as_k_best():
    # Create some test cases with varying known correct values of k. Then check that we do find them.
    for test_k in range(2, 6):
        print(test_k)
        X, y = make_blobs(500, 5, centers = test_k)
        CClust = ConsensusCluster(k_min = 2, k_max = 5, n_iter = 10)
        CClust.fit(X)
        assert CClust.k_best_ == test_k

def test_ConsensusCluster_for_k_range(test_data):
    CClust = ConsensusCluster(k_min = 2, k_max = 4, n_iter = 10)

    assert isinstance(CClust, ConsensusCluster)
    assert CClust.k_min == 2
    assert CClust.k_max == 4
    assert CClust.n_iter == 10
    assert CClust.subsample_fraction == 0.9
    assert CClust.random_state is None

    # Attributes set during init
    expected_attributes = ["k_min", "k_max", "n_iter", "subsample_fraction", "random_state"]
    for attr in expected_attributes:
        assert hasattr(CClust, attr)

    # Attributes set during fit
    CClust.fit(test_data)
    expected_attributes = ["X_", "consensus_matrix_allk_", "cluster_allk_", "labels_allk_", "k_best_", "AUC_", "AUC_delta_", "cluster_"]
    for attr in expected_attributes:
        assert hasattr(CClust, attr)

    CClust.fit(test_data)
    assert CClust.X_.shape == (100, 5)
    assert type(CClust.consensus_matrix_allk_) is dict
    assert len(CClust.consensus_matrix_allk_) == 3 # 3 because we try k =2, 3, and 4
    assert CClust.consensus_matrix_allk_[2].shape == (100, 100) # test_data has 100 instances
    assert type(CClust.cluster_allk_) is dict
    assert len(CClust.cluster_allk_) == 3
    assert type(CClust.cluster_allk_[2]) == AgglomerativeClustering
    assert type(CClust.labels_allk_) is dict
    assert len(CClust.labels_allk_) == 3
    assert CClust.labels_allk_[2].shape == (100,)
    assert type(CClust.k_best_) is np.int64
    assert type(CClust.AUC_) is dict
    assert len(CClust.AUC_) == 3
    assert type(CClust.AUC_[2]) is np.float64
    assert type(CClust.AUC_delta_) is dict
    assert len(CClust.AUC_delta_) == 3
    assert type(CClust.AUC_delta_[2]) is np.float64
    # labels_ is tested by common tests from sklearn
    assert type(CClust.cluster_) is AgglomerativeClustering


def test_ConsensusCluster_only_k_max(test_data):
    CClust = ConsensusCluster(k_max = 4, n_iter = 10)
    assert isinstance(CClust, ConsensusCluster)
    # Attributes set during init
    expected_attributes = ["k_min", "k_max", "n_iter", "subsample_fraction", "random_state"]
    for attr in expected_attributes:
        assert hasattr(CClust, attr)

    assert CClust.k_min is None
    assert CClust.k_max == 4
    assert CClust.n_iter == 10
    assert CClust.subsample_fraction == 0.9
    assert CClust.random_state is None

    # Attributes set during fit
    CClust.fit(test_data)
    expected_attributes = ["X_", "consensus_matrix_allk_", "cluster_allk_", "labels_allk_", "k_best_", "AUC_", "AUC_delta_", "cluster_"]
    for attr in expected_attributes:
        assert hasattr(CClust, attr)

    assert CClust.X_.shape == (100, 5)
    assert type(CClust.consensus_matrix_allk_) is dict
    assert len(CClust.consensus_matrix_allk_) == 1 # 1 because we only try k = 4
    assert CClust.consensus_matrix_allk_[4].shape == (100, 100) # test_data has 100 instances
    assert type(CClust.cluster_allk_) is dict
    assert len(CClust.cluster_allk_) == 1
    assert type(CClust.cluster_allk_[4]) == AgglomerativeClustering
    assert type(CClust.labels_allk_) is dict
    assert CClust.labels_allk_[4].shape == (100,)
    assert CClust.k_best_ == 4
    assert CClust.AUC_ is None
    assert CClust.AUC_delta_ is None
    # labels_ is tested by common tests from sklearn
    assert type(CClust.cluster_) is AgglomerativeClustering
