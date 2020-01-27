import logging
import numpy as np
from sklearn.cluster import SpectralClustering
from scipy.sparse import csgraph
from numpy import linalg as LA
from scipy.spatial.distance import squareform, pdist

class Regions:
    '''
    Settlements class performs DBSCAN clustering on the entire dataset of geo-coordinates
    to identify different clusters of human settlements such as cities, towns and villages
    '''
    geo_cordinates = np.array([])

    def __init__(self):
        self.logger = logging.getLogger("regions")

    def get_affinity_matrix(self, coordinates, k=7):
        """
        Calculate affinity matrix based on input coordinates matrix and the numeber
        of nearest neighbours.

        Apply local scaling based on the k nearest neighbour
            References:
        https://papers.nips.cc/paper/2619-self-tuning-spectral-clustering.pdf
        """
        self.logger.debug("Building affinity matrix")
        # calculate euclidian distance matrix
        dists = squareform(pdist(coordinates))

        # for each row, sort the distances ascendingly and take the index of the
        # k-th position (nearest neighbour)
        knn_distances = np.sort(dists, axis=0)[k]
        knn_distances = knn_distances[np.newaxis].T

        # calculate sigma_i * sigma_j
        local_scale = knn_distances.dot(knn_distances.T)

        affinity_matrix = dists * dists
        affinity_matrix = -affinity_matrix / local_scale
        # divide square distance matrix by local scale
        affinity_matrix[np.where(np.isnan(affinity_matrix))] = 0.0
        # apply exponential
        affinity_matrix = np.exp(affinity_matrix)
        np.fill_diagonal(affinity_matrix, 0)
        return affinity_matrix

    def eigen_decomposition(self, A, topK=5):
        """
        :param A: Affinity matrix
        :param plot: plots the sorted eigen values for visual inspection
        :return A tuple containing:
        - the optimal number of clusters by eigengap heuristic
        - all eigen values
        - all eigen vectors

        This method performs the eigen decomposition on a given affinity matrix,
        following the steps recommended in the paper:
        1. Construct the normalized affinity matrix: L = D−1/2ADˆ −1/2.
        2. Find the eigenvalues and their associated eigen vectors
        3. Identify the maximum gap which corresponds to the number of clusters
        by eigengap heuristic

        References:
        https://papers.nips.cc/paper/2619-self-tuning-spectral-clustering.pdf
        http://www.kyb.mpg.de/fileadmin/user_upload/files/publications/attachments/Luxburg07_tutorial_4488%5b0%5d.pdf
        """
        self.logger.debug("Computing Eigen decompostion")

        L = csgraph.laplacian(A, normed=True)
        n_components = A.shape[0]

        # LM parameter : Eigenvalues with largest magnitude (eigs, eigsh), that is, largest eigenvalues in
        # the euclidean norm of complex numbers.
        #     eigenvalues, eigenvectors = eigsh(L, k=n_components, which="LM", sigma=1.0, maxiter=5000)
        eigenvalues, eigenvectors = LA.eig(L)

        # Identify the optimal number of clusters as the index corresponding
        # to the larger gap between eigen values
        index_largest_gap = np.argmax(np.diff(eigenvalues))
        nb_clusters = index_largest_gap + 1

        self.logger.debug("Eigen decomposition applied")
        return nb_clusters, eigenvalues, eigenvectors

    def format_regions(self, labels, users):
        regions = dict()
        for region, datapoint in zip(labels, users):
            if region in regions:
                regions[region] = np.concatenate((regions[region], [datapoint]), axis=0)
            else:
                regions[region] = np.array([datapoint])

        return regions

    def detect_regions(self, users):
        '''
        Performs Spectral clustering on geo_coordinates
        :param users: geo-coordinates of all customers' locations.
        :return: dict of clusters: datapoints
        '''
        self.logger.debug("Clustering settlements")

        affinity_matrix = self.get_affinity_matrix(users, k=100)

        nb_clusters, eigenvalues, eigenvectors = self.eigen_decomposition(affinity_matrix, topK=50)
        K = nb_clusters * 1 # Adjustment factor
        self.logger.debug("Optimal K for Region Clustering " + str(K))

        region_clustering = SpectralClustering(n_clusters=K, random_state=0, affinity='precomputed')
        region_clustering.fit(affinity_matrix)

        self.regions = self.format_regions(region_clustering.labels_, users)

        return self.regions

    def locate_base_stations_proximity(self):
        self.base_stations = dict()
        for region, users in self.regions.items():
            base_station_location = np.array([
                np.mean([user[0] for user in users]),
                np.mean([user[1] for user in users])
            ])

            self.base_stations[region] = base_station_location

        return self.base_stations
