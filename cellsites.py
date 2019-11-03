from math import radians, degrees, sin, cos, asin, acos, sqrt
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
        pass

    def optimise_and_cluster(self, geo_coordinates):
        '''
        Finds optimal value of K and clusters the geo-coordianates
        :param geo_coordinates: datapoints of each settlement cluster
        :return: cluster centroids for cell sites
        '''
        K = 1
        distortion = 100

        while distortion > 80:
            cell_sites = KMeans(n_clusters=K)
            cell_sites.fit(geo_coordinates)
            distortion = sum(np.min(cdist(geo_coordinates, cell_sites.cluster_centers_, 'euclidean'), axis=1)) / geo_coordinates.shape[0]
            K += 1

        return cell_sites.cluster_centers_

    def distribute_cellsites(self, settlements):
        '''
        Optimises and distributes the cell sites
        :return: cell site distributed locations
        '''

        cellsite_locations = np.array([[None, None]])
        for settlement in settlements.values():
            cellsites_for_cluster = self.optimise_and_cluster(settlement)
            cellsite_locations = np.concatenate((cellsite_locations, cellsites_for_cluster), axis=0)

        return cellsite_locations[1:]


if __name__ == "__main__":
    import random as rd

    dataset = {}
    for i in range(10):
        datapoints = []
        for j in range(50):
            datapoints.append((rd.randrange(1000), rd.randrange(1000)))

        dataset[i] = np.array(datapoints)

    cell_sites = CellSites()
    locations = cell_sites.distribute_cellsites(dataset)
    for loc in locations:
        print(loc)