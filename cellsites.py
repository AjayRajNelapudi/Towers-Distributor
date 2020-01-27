import threading
import logging
import numpy as np
from sklearn.cluster import KMeans

class CellSites:
    '''
    CellSites considers each cluster from the Settlements class and performs K-Means clustering
    to identify the appropriate location for each cell site
    '''
    settlements = np.array([])

    def __init__(self, radiation_range):
        self.permissible_distortion = radiation_range - 0.2 * radiation_range
        self.logger = logging.getLogger("cellsites")

    def optimise_and_cluster(self, users):
        '''
        Finds optimal value of K and clusters the geo-coordianates
        :param users: datapoints of each settlement cluster
        :return: cluster centroids for cell sites
        '''
        self.logger.debug("Distributing cell sites")

        K = int(len(users) ** (1. / 3.)) - 1
        distortion = 1

        cluster_centers = np.array([])
        while distortion > self.permissible_distortion:
            K += 1
            cell_site_clustering = KMeans(n_clusters=K)
            cell_site_clustering.fit(users)
            distortion = cell_site_clustering.inertia_
            cluster_centers = cell_site_clustering.cluster_centers_
            del cell_site_clustering

        self.logger.debug("Optimal K = " + str(K))
        return cluster_centers

    def cell_site_clustering_thread(self, label, region):
        cellsites_for_cluster = self.optimise_and_cluster(region)
        self.cell_sites[label] = np.array(cellsites_for_cluster)

    def distribute_cellsites(self, regions):
        '''
        Optimises and distributes the cell sites
        :return: dict of label: cellsites
        '''
        self.logger.debug("Creating threads...")
        self.cell_sites = dict()
        clustering_threads = dict()
        for label, region in regions.items():
            clustering_thread = threading.Thread(target=self.cell_site_clustering_thread, args=(label, region))
            clustering_thread.start()
            clustering_thread.join()

            clustering_threads[label] = clustering_thread

        return self.cell_sites
