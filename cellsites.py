import logging
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

class CellSites:
    '''
    CellSites considers each cluster from the Settlements class and performs K-Means clustering
    to identify the appropriate location for each cell site
    '''
    settlements = np.array([])

    def __init__(self):
        self.logger = logging.getLogger("cellsites")

    def optimise_and_cluster(self, geo_coordinates):
        '''
        Finds optimal value of K and clusters the geo-coordianates
        :param geo_coordinates: datapoints of each settlement cluster
        :return: cluster centroids for cell sites
        '''
        self.logger.debug("Performing gradient descent")

        K = int(len(geo_coordinates) ** (1./3.))
        distortion = 1
        permissible_distortion = 0.0064 # Change permissible_distortion to vary no of towers

        while distortion > permissible_distortion:
            self.logger.debug("Applying K-Means Clustering")
            cell_sites = KMeans(n_clusters=K)
            self.logger.debug("K-Means clustering applied")
            cell_sites.fit(geo_coordinates)
            distortion = sum(np.min(cdist(geo_coordinates, cell_sites.cluster_centers_, 'euclidean'), axis=1)) / geo_coordinates.shape[0]
            self.logger.debug("K = " + str(K))
            self.logger.debug("Distortion = " + str(distortion))
            K += 1

        self.logger.debug("Optimal K = " + str(K))
        return cell_sites.cluster_centers_

    def distribute_cellsites(self, regions):
        '''
        Optimises and distributes the cell sites
        :return: dict of label: cellsites
        '''
        self.logger.debug("Distributing cellsites")
        self.cellsite_locations = dict()
        for label, region in regions.items():
            cellsites_for_cluster = self.optimise_and_cluster(region)
            self.cellsite_locations[label] = np.array(cellsites_for_cluster)
        self.logger.debug("Cellsite distribution done")

        return self.cellsite_locations
