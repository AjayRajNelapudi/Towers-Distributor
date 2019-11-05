import numpy as np
import statistics
from sklearn.cluster import SpectralClustering
from scipy.sparse import csgraph
from numpy import linalg as LA
from scipy.spatial.distance import squareform, pdist

class Settlements:
    '''
    Settlements class performs DBSCAN clustering on the entire dataset of geo-coordinates
    to identify different clusters of human settlements such as cities, towns and villages
    '''
    geo_cordinates = np.array([])

    def __init__(self):
        pass

    def get_affinity_matrix(self, coordinates, k=7):
        """
        Calculate affinity matrix based on input coordinates matrix and the numeber
        of nearest neighbours.

        Apply local scaling based on the k nearest neighbour
            References:
        https://papers.nips.cc/paper/2619-self-tuning-spectral-clustering.pdf
        """
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
        L = csgraph.laplacian(A, normed=True)
        n_components = A.shape[0]

        # LM parameter : Eigenvalues with largest magnitude (eigs, eigsh), that is, largest eigenvalues in
        # the euclidean norm of complex numbers.
        #     eigenvalues, eigenvectors = eigsh(L, k=n_components, which="LM", sigma=1.0, maxiter=5000)
        eigenvalues, eigenvectors = LA.eig(L)

        # Identify the optimal number of clusters as the index corresponding
        # to the larger gap between eigen values
        index_largest_gap = np.argsort(np.diff(eigenvalues))[::-1][:topK]
        nb_clusters = index_largest_gap + 1

        return nb_clusters, eigenvalues, eigenvectors

    def cluster_settlements(self, geo_coordinates):
        '''
        Performs Spectral clustering on geo_coordinates
        :param geo_coordinates: geo-coordinates of all customers' locations.
        :return: dict of clusters: datapoints
        '''
        affinity_matrix = self.get_affinity_matrix(geo_coordinates, k=20)
        K = len(self.eigen_decomposition(affinity_matrix, topK=7)[0])

        settlements = SpectralClustering(n_clusters=K, assign_labels='discretize', random_state=0)
        settlements.fit(geo_coordinates)

        clusters = dict()
        for cluster, datapoint in zip(settlements.labels_, geo_coordinates):
            if cluster in clusters:
                clusters[cluster] = np.concatenate((clusters[cluster], [datapoint]), axis=0)
            else:
                clusters[cluster] = np.array([datapoint])

        self.clusters = clusters
        return clusters

    def locate_base_stations(self):
        self.base_stations = dict()
        for label, users in self.clusters.items():
            base_station_location = [
                statistics.mean([user[0] for user in users]),
                statistics.mean([user[1] for user in users])
            ]

            self.base_stations[label] = np.array(base_station_location)

        return self.base_stations


if __name__ == "__main__":
    import random as rd

    datapoints = []

    for i in range(1000):
        datapoints.append([rd.uniform(17, 19), rd.uniform(82, 84)])

    settlements = Settlements()
    clusters = settlements.cluster_settlements(np.array(datapoints))
    print(clusters)