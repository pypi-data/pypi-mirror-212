import pytest

from sklearn.utils.estimator_checks import check_estimator

from skcyto import ConsensusCluster, FlowSOM
from skcyto import LogicleTransformer, HyperlogTransformer, AsinhTransformer, LogTransformer, CompensationTransformer

@pytest.mark.parametrize(
    "estimator",
    [
        ConsensusCluster(k_min = 2, k_max = 5), # check estimator only has few data points, cannot have more clusters than that
        FlowSOM(k_min = 2, k_max = 3, nodes_x=  2, nodes_y = 2), # Small grid size and few clusters, as tests of sklearn have very few instances.
        LogicleTransformer(), 
        HyperlogTransformer(), 
        AsinhTransformer(), 
        LogTransformer()
    ] 
)
def test_all_estimators(estimator):
    return check_estimator(estimator)
