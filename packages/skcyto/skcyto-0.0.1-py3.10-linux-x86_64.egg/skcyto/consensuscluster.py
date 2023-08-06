# Implemented according to original paper at https://link.springer.com/content/pdf/10.1023/A:1023949509487.pdf but only for specific FlowSOM use case as in R's FlowSOM and ConsensusClusterPlus packge

import numpy as np
from numpy.typing import NDArray
from sklearn.cluster import AgglomerativeClustering
from sklearn.base import BaseEstimator, ClusterMixin
from sklearn.utils import check_random_state
from itertools import permutations
import warnings

class ConsensusCluster(ClusterMixin, BaseEstimator):
    """Consensus clustering

    Finding the optimal number of clusters is a common problem. Consensus clustering is
    one technique, where one repeatedly subsamples the data and tries a range of number of clusters.

    This implementation currently only supports hierarchical clustering as the algorithm of choice.
    This is chosen because it is used in the R FlowSOM implementation, and because only hierarchical
    clustering guarantees that the AUC of the CDF increases when adding more clusters.
    
    Read more in Monti et al., Machine Learning 52, 91–118 (2003)

    Limitations are described in Șenbabaoğlu et al., Sci Rep. 4:6207 (2014)


    Parameters
    ----------
    k_min : int, optional
        Lower bound of number of clusters to try, by default None
        If None, only k_max is evaluated.
    k_max: int
        Upper bound of number of clusters to try, by default 20
    n_iter: int
        Number of iterations, by default 100
    subsample_fraction: float
        Fraction how many instances to sample from original data, by default 0.9.
    random_state: int, RandomState instance or None
        Determines random number generation for subsampling, by default None.

    Attributes
    ----------
    X_ : NDArray
        Input data
    k_best_ : int
        Optimal number of clusters
    cluster_ : AgglomerativeClustering
        Fitted cluster algorithm for k_best_
    labels_ : NDArray
        Labels for each instance of X with optimal number of clusters
    AUC_ : dict
        Dictionary with CDF AUC for each evaluated k
    AUC_delta_ : dict
        Dictionary with change in AUC compared to k-1 for each k
    consensus_matrix_allk_ : dict
        Dictionary with consensus matrix for each evaluated k
    cluster_allk_ : dict
        Dictionary with fitted cluster algorithm for each evaluated k
    labels_allk_ : dict
        Dictionary with labels for each instance for each evaluated k

    Raises
    ------
    ValueError
        when k_max is < 2
    ValueError
        When k_max is < k_min

    Examples
    --------
    >>> from skcyto.consensuscluster import ConsensusCluster
    >>> import numpy as np
    >>> X = np.array([[1, 2], [1, 4], [1, 0],
    ...               [10, 2], [10, 4], [10, 0]])
    >>> CClust = ConsensusCluster(k_max = 2).fit(X)
    >>> CClust.labels_
    array([1, 1, 1, 0, 0, 0])
    """
    _parameter_constraints: dict ={
        # See https://github.com/scikit-learn/scikit-learn/blob/364c77e04/sklearn/cluster/_agglomerative.py#L740 for examples
        # Useful constraints for me:
        # k_min should be None or >=2 and int
        # k_max should be >= 2 and int
        # n_iter should be int
        # subsample_fraction should be in range (0, 1]
        # random_state should be int, RandomState instance or None
    }

    def __init__(
            self,
            k_min: int = None, # If None only k_max is tried for the clustering
            k_max: int = 20, # Default from R FlowSOM implementation
            n_iter: int = 100, # Default from R FlowSOM implementation
            subsample_fraction: float = 0.9, # Default from R FlowSOM implementation. ConsensusCluster default would be 0.8
            random_state: int = None
        ):
        self.k_min = k_min
        self.k_max = k_max
        self.n_iter = n_iter
        self.subsample_fraction = subsample_fraction
        self.random_state = random_state

    def fit(self, X: NDArray, y = None):
        """Fit multiple hierarchical clustering instances, one for each candidate k.

        Parameters
        ----------
        X : NDArray
            Training data to cluster
        y : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        self: object
            Returns the fitted instance
        """
        self._validate_params()
        X = self._validate_data(X, ensure_min_samples = 2) # use the inherited function for validation instead of check_array
        self.X_ = X

        random_state = check_random_state(self.random_state)

        if self.k_max < 2:
            raise ValueError("k_max needs to be at least 2")

        if self.k_min is not None and self.k_max < self.k_min:
            raise ValueError("k_max needs to be larger than k_min")    

        k_candidates = self._construct_k_candidates()

        num_instances = X.shape[0]
        instance_ids = np.arange(num_instances)
        instances_per_subsample = round(num_instances * self.subsample_fraction)

        # Initialize dictionaries to hold info for each k
        labels_ = {}
        cluster_ = {}
        consensus_matrix_ = {} 

        for k in k_candidates:
            # i = k - self.k_min if self.k_min is not None else 0 # If k_min is None we only run this loop once, index should be 0 then

            connectivity_matrix = np.zeros(shape = (num_instances, num_instances)) # Equals M(h) from paper. Stores how often instances where in the same cluster.     
            indicator_matrix = np.zeros(shape = (num_instances, num_instances))  # Equals I(h) from paper. Stores how often instances where selected during subsampling.

            for _ in range(self.n_iter):
                # Subsample rows
                sampled_instances = random_state.choice(num_instances, size = instances_per_subsample, replace = False)
                X_subsampled = X[sampled_instances] # Equals D(h) from paper

                # Update indicator matrix for this subsampling step
                idx = np.array(list(permutations(sampled_instances, 2))).T # Use permutations to esnure that there are no problems with ordering. Otherwise indicator matrix might be updated on upper triangle, wherease connectivity matrix is updated on lowe triangle.
                indicator_matrix[idx[0], idx[1]] += 1

                # Perform subsampled clustering
                clustering_subsampled = AgglomerativeClustering(
                    n_clusters = k,
                    metric = "euclidean",
                    linkage = "average")
                labels = clustering_subsampled.fit_predict(X_subsampled)

                # Update connectivity matrix for this subsampling step
                connectivity_matrix = self._update_connectivity_matrix(
                    connectivity_matrix, 
                    instance_ids[sampled_instances], # Pass only instance ids that are present in the current subsampling
                    labels)

            # Calculate consensus matrix for this candidate k
            consensus_matrix = connectivity_matrix / (indicator_matrix + 1e-16) # 1e-16 to prevent division by 0
            np.fill_diagonal(consensus_matrix, 1) # instances are always with self in all cases where they are selected

            consensus_matrix_[k] = consensus_matrix

            # Calculate final clustering for this candidate k on consensus matrix
            clustering_final = AgglomerativeClustering(
                n_clusters = k,
                metric = "euclidean",
                linkage = "average"
            )
            cluster_[k] = clustering_final
            labels_[k] = clustering_final.fit_predict(consensus_matrix)

        self.consensus_matrix_allk_ = consensus_matrix_
        self.cluster_allk_ = cluster_
        self.labels_allk_ = labels_

        # Select best k based on consensus matrices if a range of k's was input
        if self.k_min is not None:
            self._determine_best_k()
        else:
            self.k_best_ = self.k_max
            self.AUC_ = None
            self.AUC_delta_ = None
        
        self.labels_ = self.labels_allk_[self.k_best_]
        self.cluster_ = self.cluster_allk_[self.k_best_]

        return self

    def _construct_k_candidates(self) -> NDArray:
        """Construct which values k for number of clusters to try

        Returns
        -------
        NDArray
            Cluster number candidates
        """
        if self.k_min is None:
            k_candidates = np.array([self.k_max]) # dont need to worry about AUC_delta calculation later on, as it will not  happen

        else:
            if self.k_min < 2:
                warnings.warn(UserWarning("k_min was set to below 2. Cluster numbers below 2 are not meaningful, setting it to 2."))
                self.k_min = 2

            if self.k_min == 2:
                k_candidates = np.arange(self.k_min, self.k_max + 1) # k_max + 1 because range does not contain right boundary
            else:
                k_candidates = np.arange(self.k_min - 1, self.k_max + 1) # use k_min -1 to be able to calculate the AUC_delta value for actual k_min. k_max + 1 because range does not contain right boundary

        return k_candidates

    def _update_connectivity_matrix(self, connectivity_matrix: NDArray, instance_ids: NDArray, labels: NDArray) -> NDArray:
        """Updates the connectivity matrix

        The connectivity matrix is a n x n matrix. Each entry counts the number of times that the two instances
        appeared in the same cluster. This function increments the entries for the given clustering output labels.

        Parameters
        ----------
        connectivity_matrix : NDArray
            Initial connectivity matrix
        instance_ids : NDArray
            which instance ids where looked at during this step. As we subsample instances, we need to pass which instances
            where present during the given resampling.
        labels : NDArray
            cluster output for each instance

        Returns
        -------
        NDArray
            Updated connectivity matrix
        """
        k = np.max(labels)
        idx = []
        for this_cluster in range(k + 1):
            # We dont need to handle cases where there is only 1 instance per cluster, as the empty list is removed during the flatten step
            instances_this_cluster = instance_ids[labels == this_cluster]
            combinations_this_cluster = list(permutations(instances_this_cluster, 2)) # Use with replacement as an instance is always in the same cluster as itself
            idx.append(combinations_this_cluster)

        # Flatten nested list
        idx = [item for sublist in idx for item in sublist]

        # Handle edge case where no two points are assigned to the same cluster, where we dont need to update anything.
        if len(idx) > 0:       
            idx = np.array(idx).T # For correct indexing into connectivity_matrix
            connectivity_matrix[idx[0], idx[1]] += 1

        return connectivity_matrix

    def _determine_best_k(self):
        """Determine the optimal number of clusters

        The ideal consensus matrix has only entries of 0 or 1 (either two instances never get clustered together, or always appear together).
        We can analyze the deviation from this ideal by looking at the cumulative density function of the observed consensus values of a given number of clusters.
        When a k smaller than the optimal number is chosen, the AUC of the CDF increases rapidly when adding more clusters.
        Once we reach the optimum, this change (delta AUC) slows down dramatically.
        Therefore the best k is the one after which increasing k further does no longer strongle increase the AUC (has the highest AUC_delta)
        k = 2 needs special treatment, as k=1 is not meaningful. Therefore directly use the AUC.
        """
        AUC = {}
        for k, M in self.consensus_matrix_allk_.items():
            hist, bins = np.histogram(M, bins = 100, density = True)
            AUC[k] = sum((b-a)*h for a, b, h in zip(bins[:-1], bins[1:], (np.cumsum(hist) * bins[1] - bins[0]))) # bins[1] - bins[0] gives us the binsize and normalizes the value to a proper CDF (!), because np.histogram does not do that by default.

        # Also remember that each method needs to deal with edges of k_candidates differently, as 1 needs an additional lower k, 2 needs an additional upper k
        # Method 1 similar to R ConsensusClusterPlus package
        # Does not guarantee to always get the correct k, not even in the R package (but they do it slightly differently with the ordered vector and produce nice plots in general, just the delta K is not great.)
        AUC_delta = {}
        for k in AUC.keys():
            if k == 2:
                AUC_delta[k] = AUC[k]
            else:
                AUC_delta[k] = (AUC[k] - AUC[k-1]) / AUC[k-1]

        # Method 2 similar to paper and implemented in other python packages. 
        # If this should be done, one would need to handle the k_candidates slightly differently (np.arange(self.k_min, self.k_max+2)) because then we need to have an additional element to the right of the actual range of k to try
        # AUC_delta = {}
        # for k in range(min(AUC), max(AUC)): # Use range to not iterate on the last k which is only added for evaluating k_max
        #     if k == 2:
        #         AUC_delta[k] = AUC[k]
        #     else:
        #         AUC_delta[k] = (AUC[k+1] - AUC[k]) / AUC[k]
        # AUC_delta = np.array([
        #     (A2-A1)/A1 if k>2 else A1 for A1, A2, k in zip(AUC[:-1], AUC[1:], k_candidates)
        #     ])

        k_best = max(AUC_delta, key = AUC_delta.get)

        self.AUC_ = AUC
        self.AUC_delta_ = AUC_delta
        self.k_best_ = k_best

    def fit_predict(self, X: NDArray, y = None) -> NDArray:
        """Fit and return sample's best clustering assignment.

        In addition to fitting, this method also returns the results of the
        clustering assigned with the optimal number of clusters for each
        sample in the training set.

        Parameters
        ----------
        X : NDArray
            Training instances to cluster
        y : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        NDArray
            Cluster labels
        """
        return super().fit_predict(X, y)

if __name__ == "__main__":
    test_data = np.column_stack(
        (
            np.concatenate([np.random.randn(100), np.random.randn(100) + 5, np.random.randn(100) + 10, np.random.randn(100) + 15, np.random.randn(100) + 20, np.random.randn(100) + 25]),
            np.concatenate([np.random.randn(100), np.random.randn(100) + 5, np.random.randn(100) + 10, np.random.randn(100) + 15, np.random.randn(100) + 20, np.random.randn(100) + 25])
        )
    )

    CClust = ConsensusCluster(k_min = 3, k_max = 10, n_iter = 10)
    CClust.fit(test_data)
    print(CClust.labels_)

    import matplotlib.pyplot as plt
    plt.scatter(test_data[:, 0], test_data[:, 1], c = CClust.fit_predict(test_data))
    plt.show()
