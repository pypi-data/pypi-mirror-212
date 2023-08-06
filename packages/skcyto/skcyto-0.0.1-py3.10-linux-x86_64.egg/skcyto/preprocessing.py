import numpy as np
from . import logicle_c
from numpy.typing import NDArray
from sklearn.base import BaseEstimator, TransformerMixin, OneToOneFeatureMixin
from sklearn.utils.validation import check_is_fitted

class LogicleTransformer(BaseEstimator, TransformerMixin, OneToOneFeatureMixin):
    """Logicle Transformation

    Implemented according to GatingML2.0 specification.

    See also
        Moore WA and Parks DR. Update for the logicle data scale including operational
        code implementations. Cytometry A., 2012:81A(4):273–277.

    Parameters
    ----------
    t : float
        Upper bound of the linear scale, by default 262144
    m : float
        Number of decades for the logarithmic scale, by default 4.5
    w : float
        Number of decades for linear scale, by default 0.5
    a : float
        Number of negative decades, by default 0
    """
    _parameter_constraints: dict ={
    }
    def __init__(self,
                 t: float = 262144, 
                 m: float = 4.5, 
                 w: float = 0.5, 
                 a: float = 0):
        self.t = t
        self.m = m
        self.w = w
        self.a = a

    def _reset(self):
        if hasattr(self, "n_samples_seen_"):
            del self.n_samples_seen_

    def fit(self, X: NDArray, y: NDArray = None):
        """Fit only validates parameters and data, as everything is defined by the user.

        X : NDArray
            Input data
        y : Ignored.
            Not used, only present for API conventions.
        """
        self._validate_params()

        self._reset()
        first_pass = not hasattr(self, "n_samples_seen_")
        X = self._validate_data(
            X,
            reset = first_pass, # To set n_features_in_ attribute or check against it.
            force_all_finite = True
            )

        if first_pass:
            self.n_samples_seen_ = X.shape[0]
        else:
            self.n_samples_seen_ += X.shape[0]


        return self

    def transform(self, X: NDArray) -> NDArray:
        """Transform according to specified logicle

        Parameters
        ----------
        X : NDArray
            Data

        Returns
        -------
        NDArray
            Transformed data
        """
        check_is_fitted(self)
        X = self._validate_data(
            X,
            reset = False,
            force_all_finite = True
        )
        X = X.copy()
        for i in range(X.shape[1]):
            X[:, i] = logicle_c.logicle_scale(self.t, self.w, self.m, self.a, X[:, i])

        return X
    
    def inverse_transform(self, X: NDArray) -> NDArray:
        """Perform inverse logicle transform

        Parameters
        ----------
        X : NDArray
            Input data

        Returns
        -------
        NDArray
            inversely transformed data
        """
        check_is_fitted(self)
        X = self._validate_data(
            X,
            reset = False,
            force_all_finite = True
        )
        X = X.copy()

        for i in range(X.shape[1]):
            X[:, i] = logicle_c.logicle_inverse(self.t, self.w, self.m, self.a, X[:, i])

        return X

    def fit_transform(self, X: NDArray, y = None) -> NDArray:
        """Fit and transform data

        As fit does not doo anything, this is identical to just running transform and is
        only implemented for API conventions.

        Parameters
        ----------
        X : NDArray
            Input data
        y : Ignored.
            Not used, only present for API conventions.

        Returns
        -------
        NDArray
            Transformed data
        """
        return super().fit_transform(X, y)
    
class HyperlogTransformer(BaseEstimator, TransformerMixin, OneToOneFeatureMixin):
    """Hyperlog transform

    Implemented according to GatingML2.0 specification.

    See also
        Bagwell CB. Hyperlog-a flexible log-like transform for negative, zero, and
        positive valued data. Cytometry A., 2005:64(1):34–42.

    Parameters
    ----------
    t : float
        Upper bound of the linear scale, by default 262144
    m : float
        Number of decades for the logarithmic scale, by default 4.5
    w : float
        Number of decades for linear scale, by default 0.5
    a : float
        Number of negative decades, by default 0
    """
    _parameter_constraints: dict ={
    }

    def __init__(self,
                 t: float = 262144, 
                 m: float = 4.5, 
                 w: float = 0.5, 
                 a: float = 0):
        self.t = t
        self.m = m
        self.w = w
        self.a = a

    def _reset(self):
        if hasattr(self, "n_samples_seen_"):
            del self.n_samples_seen_

    def fit(self, X: NDArray, y: NDArray = None):
        """Fit only validates parameters and data, as everything is defined by the user.

        X : NDArray
            Input data
        y : Ignored.
            Not used, only present for API conventions.
        """
        self._validate_params()

        first_pass = not hasattr(self, "n_samples_seen_")
        X = self._validate_data(
            X,
            reset = first_pass, # To set n_features_in_ attribute or check against it.
            force_all_finite = True
            )

        if first_pass:
            self.n_samples_seen_ = X.shape[0]
        else:
            self.n_samples_seen_ += X.shape[0]

        return self

    def transform(self, X: NDArray) -> NDArray:
        """Transform according to specified hyperlog

        Parameters
        ----------
        X : NDArray
            Data

        Returns
        -------
        NDArray
            Transformed data
        """
        check_is_fitted(self)
        X = self._validate_data(
            X,
            reset = False,
            force_all_finite = True
        )
        X = X.copy()

        for i in range(X.shape[1]):
            X[:, i] = logicle_c.hyperlog_scale(self.t, self.w, self.m, self.a, X[:, i])

        return X
    
    def inverse_transform(self, X: NDArray) -> NDArray:
        """Perform inverse hyperlog transform

        Parameters
        ----------
        X : NDArray
            Input data

        Returns
        -------
        NDArray
            inversely transformed data
        """
        check_is_fitted(self)
        X = self._validate_data(
            X,
            reset = False,
            force_all_finite = True)

        X = X.copy()
        for i in range(X.shape[1]):
            X[:, i] = logicle_c.hyperlog_inverse(self.t, self.w, self.m, self.a, X[:, i])

        return X

    def fit_transform(self, X: NDArray, y = None) -> NDArray:
        """Fit and transform data

        As fit does not doo anything, this is identical to just running transform and is
        only implemented for API conventions.

        Parameters
        ----------
        X : NDArray
            Input data
        y : Ignored.
            Not used, only present for API conventions.

        Returns
        -------
        NDArray
            Transformed data
        """
        return super().fit_transform(X, y)

class AsinhTransformer(BaseEstimator, TransformerMixin, OneToOneFeatureMixin):
    """Parametrized Arcsinh transform

    Implemented according to GatingML2.0 specification
    Note that this is equivalent to a logicle transform with w = 0

    Parameters
    ----------
    t : float
        Upper bound of the linear scale, by default 262144
    m : float
        Number of decades for the logarithmic scale, by default 4.5
    a : float
        Number of negative decades, by default 0
    """
    _parameter_constraints: dict ={
    }
    def __init__(self,
                 t: float = 262144, 
                 m: float = 4.5, 
                 a: float = 0):
        self.t = t
        self.m = m
        self.a = a

    def _reset(self):
        if hasattr(self, "n_samples_seen_"):
            del self.n_samples_seen_

    def fit(self, X: NDArray, y: NDArray = None):
        """Fit only validates parameters and data, as everything is defined by the user.

        X : NDArray
            Input data
        y : Ignored.
            Not used, only present for API conventions.
        """
        self._validate_params()

        self._reset()
        first_pass = not hasattr(self, "n_samples_seen_")
        X = self._validate_data(
            X,
            reset = first_pass, # To set n_features_in_ attribute or check against it.
            force_all_finite = True
            )

        if first_pass:
            self.n_samples_seen_ = X.shape[0]
        else:
            self.n_samples_seen_ += X.shape[0]
        
        return self


    def transform(self, X: NDArray) -> NDArray:
        """Transform according to specified asinh transform

        Parameters
        ----------
        X : NDArray
            Data

        Returns
        -------
        NDArray
            Transformed data
        """
        check_is_fitted(self)
        X = self._validate_data(
            X,
            reset = False,
            force_all_finite = True
        )

        X = X.copy()
        for i in range(X.shape[1]):
            X[:, i] = logicle_c.logicle_scale(self.t, 0, self.m, self.a, X[:, i])

        return X
    
    def inverse_transform(self, X: NDArray) -> NDArray:
        """Perform inverse asinh transform

        Parameters
        ----------
        X : NDArray
            Input data

        Returns
        -------
        NDArray
            inversely transformed data
        """
        check_is_fitted(self)
        X = self._validate_data(
            X,
            reset = False,
            force_all_finite = True
            )

        X = X.copy()
        for i in range(X.shape[1]):
            X[:, i] = logicle_c.logicle_inverse(self.t, 0, self.m, self.a, X[:, i])

        return X

    def fit_transform(self, X: NDArray, y = None) -> NDArray:
        """Fit and transform data

        As fit does not doo anything, this is identical to just running transform and is
        only implemented for API conventions.

        Parameters
        ----------
        X : NDArray
            Input data
        y : Ignored.
            Not used, only present for API conventions.

        Returns
        -------
        NDArray
            Transformed data
        """
        return super().fit_transform(X, y)
    
class LogTransformer(BaseEstimator, TransformerMixin, OneToOneFeatureMixin):
    """Parametrized Log transform

    Implemented according to GatingML2.0 specification.

    Parameters
    ----------
    t : float
        Upper bound of the linear scale, by default 262144
    m : float
        Number of decades for the logarithmic scale, by default 4.5
    """
    _parameter_constraints: dict ={
    }

    def __init__(self,
                 t: float = 262144, 
                 m: float = 4.5):
        self.t = t
        self.m = m

    def _reset(self):
        if hasattr(self, "n_samples_seen_"):
            del self.n_samples_seen_

    def fit(self, X: NDArray, y: NDArray = None):
        """Fit only validates parameters and data, as everything is defined by the user.

        X : NDArray
            Input data
        y : Ignored.
            Not used, only present for API conventions.
        """
        self._validate_params()

        self._reset()
        first_pass = not hasattr(self, "n_samples_seen_")
        X = self._validate_data(
            X,
            reset = first_pass, # To set n_features_in_ attribute or check against it.
            force_all_finite = True
            )

        if first_pass:
            self.n_samples_seen_ = X.shape[0]
        else:
            self.n_samples_seen_ += X.shape[0]
        
        return self

    def transform(self, X: NDArray) -> NDArray:
        """Transform according to specified log transform

        Parameters
        ----------
        X : NDArray
            Data

        Returns
        -------
        NDArray
            Transformed data
        """
        check_is_fitted(self)
        X = self._validate_data(
            X,
            reset = False,
            force_all_finite = True
        )

        X = X.copy()
        for i in range(X.shape[1]):
            X[:, i] = ((1 / self.m) * np.log10(X[:, i] / self.t) + 1).flatten()

        return X
    
    def inverse_transform(self, X: NDArray) -> NDArray:
        """Perform inverse log transform

        Parameters
        ----------
        X : NDArray
            Input data

        Returns
        -------
        NDArray
            inversely transformed data
        """
        check_is_fitted(self)
        X = self._validate_data(
            X,
            reset = False,
            force_all_finite = True
            )

        X = X.copy()
        for i in range(X.shape[1]):
            X[:, i] = 10 ** ((X[:, i] - 1) * self.m) * self.t

        return X

    def fit_transform(self, X: NDArray, y = None) -> NDArray:
        """Fit and transform data

        As fit does not doo anything, this is identical to just running transform and is
        only implemented for API conventions.

        Parameters
        ----------
        X : NDArray
            Input data
        y : Ignored.
            Not used, only present for API conventions.

        Returns
        -------
        NDArray
            Transformed data
        """
        return super().fit_transform(X, y)

class CompensationTransformer(BaseEstimator, TransformerMixin, OneToOneFeatureMixin):
    def __init__(self, C: NDArray):
        self.C = C

    def fit(self, X: NDArray, y: NDArray = None):
        """Fit only checky compatibility between input data and compensation matrix.

        X : NDArray
            Input data
        y : Ignored.
            Not used, only present for API conventions.
        """
        X = self._validate_data(
            X,
            force_all_finite=True)

        self._check_X_C_compatible(X)
        return self

    def transform(self, X: NDArray) -> NDArray:
        """Compensate data with specified compensation matrix

        Parameters
        ----------
        X : NDArray
            Data

        Returns
        -------
        NDArray
            Compensated data
        """
        X = self._validate_data(
            X,
            force_all_finite=True)

        self._check_X_C_compatible(X)

        X = np.linal.solve(self.C.T, X.T).T

        return X
    
    def inverse_transform(self, X: NDArray) -> NDArray:
        """Decompensate data

        Parameters
        ----------
        X : NDArray
            Input data

        Returns
        -------
        NDArray
            Decompensated data
        """
        X = self._validate_data(
            X,
            force_all_finite=True)

        self._check_X_C_compatible(X)

        X = np.linal.solve(X, self.C)

        return X

    def fit_transform(self, X: NDArray, y = None) -> NDArray:
        """Fit and transform data

        As fit does not doo anything, this is identical to just running transform and is
        only implemented for API conventions.

        Parameters
        ----------
        X : NDArray
            Input data
        y : Ignored.
            Not used, only present for API conventions.

        Returns
        -------
        NDArray
            Compensated data
        """
        return super().fit_transform(X, y)
    
    def _check_X_C_compatible(self, X:NDArray):
        if self.C.shape[1] != X.shape[1]:
            raise ValueError("Compensation matrix is incompatible with data.")
    
# Flin transformation is MinMaxScaler

