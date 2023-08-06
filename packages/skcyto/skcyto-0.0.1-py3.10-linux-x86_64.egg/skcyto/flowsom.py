import numpy as np
from numpy.typing import NDArray
import igraph as ig
from sklearn.base import BaseEstimator, ClusterMixin
from sklearn.utils.validation import check_array, check_is_fitted
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy.spatial.distance import pdist, squareform
from minisom import MiniSom, asymptotic_decay
from .consensuscluster import ConsensusCluster
import matplotlib.pyplot as plt

def get_group_means(X: NDArray, labels: NDArray) -> dict:
    """Calculates mean per group and feature

    Parameters
    ----------
    X : NDArray
        Data to calculate on
    labels : NDArray
        groups

    Returns
    -------
    dict
        Dictionary with means per group
    """
    return {label: np.mean(X[labels == label], axis = 0) for label in np.unique(labels)}

def get_group_cv(X: NDArray, labels: NDArray) -> dict:
    """Calculates coefficient of variation per group and feature

    Parameters
    ----------
    X : NDArray
        Data to calculate on
    labels : NDArray
        groups

    Returns
    -------
    dict
        Dictionary with CV per group
    """
    unique_labels = np.unique(labels)
    means = np.array([np.mean(X[labels == label], axis = 0) for label in unique_labels])
    stds = np.array([np.std(X[labels == label], axis = 0) for label in unique_labels])
    cvs = stds / means

    return {label: cvs[i, :] for i, label in enumerate(unique_labels)}



class FlowSOM(BaseEstimator, ClusterMixin):
    """FlowSOM algorithm to cluster cytometry data

    Trains a FlowSOM algorithm on the given data. Follows the original R implementation
    as closely as possible. 

    See also the original publication: 

    Van Gassen et al., FlowSOM: Using self-organizing maps for visualization and interpretation of cytometry data. Cytometry A. (2015)

    Parameters
    ----------
    nodes_x : int
        Number of SOM nodes in X direction, by default 10
    nodes_y : int
        Number of SOM nodes in Y direction, by default 10
    n_iter : int
        Number of iterations to train SOM, by default 10
    learning_rate : float
        Learning rate of the SOM, by default 0.5
    neighborhood_function : str
        Neighborhood function of the SOM, by default gaussian
    sigma : float
        Standard deviation of the SOM's neighborhood function, by default 1
    activation_distance : string
        Distance function for SOM, by default euclidean
    k_min : int, optional
        Lower bound for metaclustering number of clusters, by default None
    k_max : int
        Upper bound for metaclustering number of clusters, by default 20
    random_state: int, RandomState instance or None
        Determines random number generation for SOM training and 
        ConsensusClustering subsampling, by default None.

    Attributes
    ----------
    X_ : NDArray
        Training data
    labels_ : 
        Labels for each instance of X after SOM assignment and metaclustering
    importance_ : NDArray
        Importances, if specified during fit
    n_nodes_ : int
        Number of SOM nodes
    som_ : MiniSOM
        Trained SOM model
    som_weights_ : NDArray
        Weights of SOM nodes. Shape (n_nodes_, n_features)
    som_labels_ : NDArray
        Assigned SOM node for each sample in X
    mst_ : Graph
        Minimal-spanning-tree of the SOM nodes
    n_clusters_ : int
        Number of metaclusters
    som_metacluster_labels_ : NDArray
        Metacluster label of each SOM node. Shape (n_nodes,)
    consensus_clustering_ : ConsensusCluster
        ConsensusCluster object used for metaclustering

    Examples
    --------
    >>> from skcyto import FlowSOM
    >>> import numpy as np
    >>> X = np.array([[1, 2], [1, 4], [1, 0],
    ...               [10, 2], [10, 4], [10, 0]])
    >>> fsom = FlowSOM(k_min = 2, k_max = 3, nodes_x=  2, nodes_y = 2)
    >>> fsom.fit(X)
    >>> fsom.labels_
    array([0, 0, 1, 2, 2, 2])
    """
    def __init__(
        # SOM args
        self, 
        nodes_x: int = 10,
        nodes_y: int = 10,
        n_iter: int = 10,
        learning_rate: float = 0.5,
        neighborhood_function: str = "gaussian", 
        sigma: float = 1.0, 
        activation_distance: str = "euclidean", 
        # Args for metaclustering
        k_min: int = None,
        k_max: int = 20,
        random_state: int = None
        ):
        # SOM args
        self.nodes_x = nodes_x
        self.nodes_y = nodes_y
        self.n_iter = n_iter
        self.learning_rate = learning_rate
        self.neighborhood_function = neighborhood_function
        self.sigma = sigma
        self.activation_distance = activation_distance

        # Metaclustering args
        self.k_min = k_min
        self.k_max = k_max
    
        self.random_state = random_state

            

    def fit(self, X: NDArray, y = None, importance: NDArray = None): # Scale parameters by these factors.
        """Fit FlowSOM to data

        Parameters
        ----------
        X : NDArray
            Training data to cluster
        y : Ignored
            Not used, present here for API consistency by convention.
        importance : NDArray, optional
            Can be used to scale individual features to give them more importance during training, by default None

        Returns
        -------
        self: object
            Returns the fitted instance

        Raises
        ------
        ValueError
            If importance is specified and its shape is not matching X
        """
        X = check_array(X)
        self.n_features_in_ = X.shape[1] # This replaces input_len. To make it sklearn compatible this needs to be set at train time.

        if importance is not None:
            if importance.shape[1] != X.shape[1]:
                raise ValueError("Importance must have exactly one entry for each feature in X")
            
            X = X * importance

        self.importance_ = importance
        self.X_ = X
        self.n_nodes_ = self.nodes_x * self.nodes_y

        self._construct_SOM()
        self._construct_MST()
        self._consensus_cluster()

        return self


    def _construct_SOM(self):
        """Train the self-organizing map for the data
        """
        # SOM + metaclustering code goes here
        som = MiniSom(
            x = self.nodes_x,
            y = self.nodes_y,
            input_len = self.n_features_in_,
            sigma = self.sigma,
            learning_rate = self.learning_rate,
            neighborhood_function = self.neighborhood_function,
            activation_distance = self.activation_distance,
            random_seed = self.random_state,
            topology = "rectangular",
            decay_function = asymptotic_decay

        )

        som.train(
            self.X_, 
            num_iteration = self.n_iter, 
            random_order = False,
            use_epochs = False,
            verbose = False
            )

        self.som_ = som
        # Reshape weights to be in same format as input data (i.e. each row is one som point with corresponding features)
        self.som_weights_ = som.get_weights().reshape((-1, self.n_features_in_))

        # Calculate cluster labels from som by associating each data point with its closest node
        winner_coordinates = np.array([som.winner(x) for x in self.X_]).T
        self.som_labels_ = np.ravel_multi_index(winner_coordinates, (self.nodes_x, self.nodes_y))


    def _construct_MST(self):
        """Generate the minimal-spanning-tree for the SOM nodes
        """
        adjacency_matrix = squareform(pdist(self.som_weights_, "euclidean"))
        g = ig.Graph.Weighted_Adjacency(matrix = adjacency_matrix, mode = "undirected", loops = False)
        self.mst_ = g.spanning_tree(weights = g.es["weight"]) # Uses Prim algorithm, as in R, which also uses igraph under the hood.

    def _consensus_cluster(self):
        """Performs consensus clustering on SOM nodes
        """
        # FlowSom only ever uses hierarchical clustering, even though many other possibilities are implemented. Linkage is average linkage.
        CClust = ConsensusCluster(k_min = self.k_min, k_max = self.k_max, n_iter = 100, subsample_fraction = 0.9, random_state = self.random_state)
        CClust.fit(self.som_weights_)

        # If required, find optimal number of clusters based on elbow method. R implementation does not rely on k_best found by ConsensusCluster!
        if self.k_min is not None:
            WSS = [self._calc_within_cluster_sum_squared_error(self.som_weights_, labels) for _, labels in CClust.labels_allk_.items()]
            # R packages smoothes WSS for better elbow finding, replicated here
            WSS = self._smooth(WSS)

            self.n_clusters_ = int( # Transform to int because we always have integer number of clusters and otherwise indexing to labels_allk_ doesnt work
                self._find_elbow(
                    np.fromiter(CClust.labels_allk_.keys(), dtype = int).reshape(-1, 1), 
                    np.array(WSS).reshape(-1, 1)
                )
            )
            self.som_metacluster_labels_ = CClust.labels_allk_[self.n_clusters_]
            
        else:
            self.n_clusters_ = self.k_max
            self.som_metacluster_labels_ = CClust.labels_

        self.consensus_clustering_ = CClust

        # Finally map each instance of X to the som node, and the som node to the metacluster
        self.labels_ = self._map_X_to_metacluster_label(self.X_)
        
    def _calc_within_cluster_sum_squared_error(self, X: NDArray, y: NDArray) -> float:
        """Calculate within cluster sum of squared errors

        Parameters
        ----------
        X : NDArray
            The data of all instances

        y : NDArray
            The labels of all instances

        Returns
        -------
        float
            Within cluster sum of squared errors
        """
        WSS = 0
        for this_cluster in np.unique(y):
            WSS += np.sum(np.var(X[y == this_cluster, :], 0))

        return WSS
    
    def _smooth(self, x: NDArray, smooth = 0.2) -> NDArray:
        """Linear smoothing 

        This function performs linear smoothing of the point with its closest neighbors
        Passed in x is not modified, as it is copied internally.
        
        Parameters
        ----------
        x : NDArray
            values to smooth
        smooth : float, optional
            linear smoothing factor, by default 0.2

        Returns
        -------
        NDArray
            smoothed version of x
        """
        x = x.copy() # Prevent modifying x by reference
        x_orig = x.copy()
        # Performs linear smoothing with neighbors
        # Boundaries are not modified
        # R performs smoothing interatively, i.e. when position i is accessed, position i-1 has already been smoothed in the previous step!
        for i in range(1, len(x)-1):
            x[i] = (1-smooth) * x_orig[i] + (smooth/2) * x_orig[i-1] + (smooth/2) * x_orig[i+1]
        
        return x

    
    def _find_elbow(self, X: NDArray, y: NDArray) -> float:
        """Find elbow of a plot

        Parameters
        ----------
        X : NDArray
            X values
        y : NDArray
            y values

        Returns
        -------
        float
            point x from array X where the plot has an elbow
        """
        # Fit 2 linear regression to all possible splits of the vector
        # The split point where sum of residuals of both regressions is smallest is the elbow of the plot and the best number of clusters
        optimal = 0
        min_residuals = np.Inf

        for i in range(1, len(y)):
            lr_1 = LinearRegression().fit(X[:i], y[:i])
            residual_1 = mean_squared_error(lr_1.predict(X[:i]), y[:i])

            lr_2 = LinearRegression().fit(X[i:], y[i:])
            residual_2 = mean_squared_error(lr_2.predict(X[i:]), y[i:])

            residuals = residual_1 + residual_2

            if residuals < min_residuals:
                optimal = i
                min_residuals = residuals

        return X[optimal]
    
    def _map_X_to_som(self, X: NDArray) -> NDArray:
        """Maps each sample in X to the nearest SOM node

        Parameters
        ----------
        X : NDArray
            Data

        Returns
        -------
        NDArray
            SOM labels
        """
        out = []
        for x in X:
            winner_coordinates = self.som_.winner(x)
            out.append(np.ravel_multi_index(winner_coordinates, (self.nodes_x, self.nodes_y)))

        return np.array(out)

    def _map_X_to_metacluster_label(self, X: NDArray) -> NDArray:
        """Maps each instance in X to its metacluster

        Each instance is first mapped to the closes SOM node. Then the label of this SOM node
        is retrieved from the stored cluster result.

        Parameters
        ----------
        X : NDArray
            Input array

        Returns
        -------
        NDArray
            Metacluster labels
        """
        winner_ids = self._map_X_to_som(X)
        return self.som_metacluster_labels_[winner_ids]
        
    def get_som_MFI(self) -> dict:
        """Calculates mean fluorescence intensity of each SOM node

        If a node has no cells associated to it, it is not in the returned dict.

        Returns
        -------
        dict
            Dictionary with mean intensity per SOM node
        """
        check_is_fitted(self)
        return get_group_means(self.som_labels_, self.X_)

    def get_metacluster_MFI(self) -> dict:
        """Calculates mean fluorescence intensity of each metacluster

        Returns
        -------
        dict
            Dictionary with mean intensity per metacluster
        """
        check_is_fitted(self)
        return get_group_means(self.metacluster_labels_, self.X_)        
       
    def get_som_CV(self) -> dict:
        """Calculates coefficient of variation for all channels of each SOM node

        If a node has no cells associated to it, it is not in the returned dict.

        Returns
        -------
        dict
            Dictionary with CV per channel and SOM node
        """
        check_is_fitted(self)
        return get_group_cv(self.som_labels_, self.X_)
    
    def get_metacluster_CV(self) -> dict:
        """Calculates coefficient of variation for all channels of each metacluster

        Returns
        -------
        dict
            Dictionary with CV per channel and metacluster
        """
        check_is_fitted(self)
        return get_group_cv(self.metacluster_labels_, self.X_)
    
    def get_som_counts(self) -> dict:
        """Calculates cell counts per SOM node

        If a node has no cells associated to it, it is not in the returned dict.

        Returns
        -------
        dict
            Dictionary with cell count per SOM node
        """
        check_is_fitted(self)
        id, count = np.unique(self.som_labels_, return_counts = True)
    
        return dict(zip(id, count))
    
    def get_metacluster_counts(self) -> dict:
        """Calculates cell counts per metacluster

        Returns
        -------
        dict
            Dictionary with cell count per metacluster
        """
        check_is_fitted(self)
    
        id, count = np.unique(self.metacluster_labels_, return_counts = True)
    
        return dict(zip(id, count))
    
    def get_som_percentages(self) -> dict:
        """Calculates percentage of total cells assigned to each SOM node

        If a node has no cells associated to it, it is not in the returned dict.

        Returns
        -------
        dict
            Dictionary cell percentage per SOM node
        """
        check_is_fitted(self)

        id, count = np.unique(self.som_labels_, return_counts = True)
    
        return dict(zip(id, count/len(self.som_labels_)))
    
    def get_metacluster_percentages(self) -> dict:
        """Calculates percentage of total cells assigned to each metacluster

        Returns
        -------
        dict
            Dictionary cell percentage per metacluster
        """
        check_is_fitted(self)

        id, count = np.unique(self.metacluster_labels_, return_counts = True)
    
        return dict(zip(id, count/len(self.metacluster_labels_)))

    def get_outliers(self, X: NDArray, n_mad: float = 5) -> NDArray:
        """Determine which cells are outliers to their assigned SOM node, based on MAD.

        For each cell, the euclidean distance to its SOM node is calculated.
        For each SOM node, the median and mean absolute deviaton from the median is calculated.
        A cell is considered an outlier, if it is further away than median + n_mad * mad away from its assigned node center.

        Parameters
        ----------
        X : NDArray
            Array with measured cells
        n_mad : float, optional
            Factor how many times of MAD a cell can be away from the SOM center, by default 5

        Returns
        -------
        NDArray
            Boolean array indicating whether a cell is an outlier.
        """
        check_is_fitted(self)
        winner_ids = self._map_X_to_som(X)
        
        # Extract corresponding SOM node center for each cell
        centers = self.som_weights_[winner_ids]
        # Calculate euclidean distance of cell to its assigned node center
        distances = np.array([np.linalg.norm(X[i] - centers[i]) for i in range(X.shape[0])])

        # For each center, calculate the median of the cell distances to it, and the mean absolute deviation from the median 
        unique_winner_ids = np.unique(winner_ids)       
        distance_medians = np.array([np.median(distances[winner_ids == winner_id]) for winner_id in unique_winner_ids])
        distance_mads = np.array([
            np.mean(
                np.absolute(
                    np.median(distances[winner_ids == winner_id]) - distances[winner_ids == winner_id]
                )
            ) for winner_id in unique_winner_ids])
        
        # For each node center, calculate the threshold
        distance_thresholds = distance_medians + distance_mads * n_mad

        # distance_thresholds only contains the threshold for each center.
        # But we want to compare the distance of each cell. Therefore need to compare the distance of each cell to the corresponding threshold.
        # I didnt find a better way to do the indexing unfortunately
        distance_thresholds = dict(zip(distance_thresholds)) 
        distance_thresholds = np.array([distance_thresholds[i] for i in winner_ids])
        is_outlier = distances > distance_thresholds

        return is_outlier


    def plot_MST(self, grid_layout : bool = False):
        """Plot the minimal spanning tree

        Parameters
        ----------
        grid_layout : bool, optional
            Whether to plot MST in grid layout, by default False
        """
        fig, ax = plt.subplots()
        if grid_layout:
            layout = "grid"
        else:
            layout = "auto"

        ig.plot(
            self.mst_,
            target = ax,
            layout = layout
        )
        plt.show()

    def fit_predict(self, X: NDArray, y: NDArray = None, importance: NDArray = None) -> NDArray:
        """Fit and return the metacluster labels of each sample

        Features can be weighted by a user-specified importance, if desired.

        Parameters
        ----------
        X : NDArray
            Training instances to cluster
        y : NDArray, optional
            Not used, present here for API consistency by convention.
        importance : NDArray, optional
            Weights to scale each feature by during analysis, by default None

        Returns
        -------
        NDArray
            Metacluster labels
        """
        self.fit(X, y, importance)
        return self.labels_

    def predict(self, X: NDArray) -> NDArray:
        """Predicts the metacluster label for each sample in X

        Parameters
        ----------
        X : NDArray
            Measurements

        Returns
        -------
        NDArray
            Metacluster labels
        """
        # Predicts metacluster label!
        check_is_fitted(self)
        X = check_array(X)
        
        return self._map_X_to_metacluster_label(X)
    
    def predict_som(self, X: NDArray) -> NDArray:
        """Predicts only the SOM node label for each instance in X

        Parameters
        ----------
        X : NDArray
            Measurements

        Returns
        -------
        NDArray
            SOM node labels
        """
        # Predicts only the SOM node of an input array
        check_is_fitted(self)
        X = check_array(X)
        
        return self._map_X_to_som(X)

if __name__ == "__main__":
    test_data = np.column_stack(
        (
            np.concatenate([np.random.randn(100), np.random.randn(100) + 5, np.random.randn(100) + 10, np.random.randn(100) + 15, np.random.randn(100) + 20, np.random.randn(100) + 25]),
            np.concatenate([np.random.randn(100), np.random.randn(100) + 5, np.random.randn(100) + 10, np.random.randn(100) + 15, np.random.randn(100) + 20, np.random.randn(100) + 25])
        )
    )

    fsom = FlowSOM(k_min = 3, k_max = 7)
    fsom.fit(test_data)
    fsom._get_outliers(test_data)    