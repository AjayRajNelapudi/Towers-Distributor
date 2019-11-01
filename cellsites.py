import numpy
from sklearn.cluster import KMeans

class CellSites:
    '''
    CellSites considers each cluster from the Settlements class and performs K-Means clustering
    to identify the appropriate location for each cell site
    '''
    def __init__(self):
        pass

    def cluster_settlement(self):
        '''
        Performs K-Means clustering on the given datapoints of geo-coordinates
        :return: K centroids
        '''
        pass

    def identify_cell_site_count(self):
        '''
        Iterates and finds value of K where the mean squared distance is less than 0.8 km
        :return: k value
        '''
        pass