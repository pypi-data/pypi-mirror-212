import pytest
import numpy as np
from numpy.testing import assert_allclose
from skcyto.preprocessing import LogicleTransformer, HyperlogTransformer, AsinhTransformer, LogTransformer, CompensationTransformer

@pytest.fixture
def test_data():
    X = np.array([-10, -5, -1, 0, 0.3, 1, 3, 10, 100, 1000]).reshape(-1, 1)
    return X

def test_logicle(test_data):
    X_expected = np.array([[-0.32991448],
       [-0.25997887],
       [-0.08827359],
       [ 0.11111111],
       [ 0.19407499],
       [ 0.31049581],
       [ 0.42925969],
       [ 0.5521367 ],
       [ 0.77743341],
       [ 1.        ]])
    
    logicle = LogicleTransformer(t = 1000)
    expected_attributes = ["t", "w", "m", "a"]
    for attr in expected_attributes:
        assert hasattr(logicle, attr)
    
    X = logicle.fit_transform(test_data)
    assert_allclose(X, X_expected)

    X_retransformed = logicle.inverse_transform(X)
    assert_allclose(X_retransformed, test_data)

def test_hyperlog(test_data):
    X_expected = np.array(
        [[-0.32199612],
       [-0.24711165],
       [-0.06294153],
       [ 0.11111111],
       [ 0.18009953],
       [ 0.28516375],
       [ 0.41167614],
       [ 0.54421834],
       [ 0.77627007],
       [ 1.        ]])
    hyperlog = HyperlogTransformer(t = 1000)
    X = hyperlog.fit_transform(test_data)
    assert_allclose(X, X_expected)

    X_retransformed = hyperlog.inverse_transform(X)
    assert_allclose(X_retransformed, test_data)

def test_asinh(test_data):
    X_expected = np.array(
        [[-0.55555652],
       [-0.48866386],
       [-0.3334297 ],
       [ 0.        ],
       [ 0.21819295],
       [ 0.3334297 ],
       [ 0.439371  ],
       [ 0.55555652],
       [ 0.77777779],
       [ 1.        ]])
    
    asinh = AsinhTransformer(t = 1000)
    X = asinh.fit_transform(test_data)
    assert_allclose(X, X_expected)

    X_retransformed = asinh.inverse_transform(X)
    assert_allclose(X_retransformed, test_data)

@pytest.mark.filterwarnings("ignore::RuntimeWarning") # Ignore division by zero and na value warning 
def test_log(test_data):
    X_expected = np.array(
        [[    np.nan],
       [    np.nan],
       [    np.nan],
       [   -np.inf],
       [0.21713806],
       [0.33333333],
       [0.43936028],
       [0.55555556],
       [0.77777778],
       [1.        ]])
    log = LogTransformer(t = 1000)
    X = log.fit_transform(test_data)
    assert_allclose(X, X_expected)

    # Cannot check retransform from X directly as nan and inf are not supported
    assert_allclose(log.inverse_transform(X[4:]), test_data[4:])