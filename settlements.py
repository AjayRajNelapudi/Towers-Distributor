import numpy as np
from sklearn.cluster import DBSCAN

class Settlements:
    '''
    Settlements class performs DBSCAN clustering on the entire dataset of geo-coordinates
    to identify different clusters of human settlements such as cities, towns and villages
    '''
    # max_distance =
    min_samples = 250
    geo_cordinates = np.array([])

    def __init__(self, geo_coordinates):
        self.geo_coordinates = geo_coordinates

    def cluster_all_settlements(self):
        '''
        Performs DBSCAN clustering on self.geo_coordinates
        :return:
        '''
        pass