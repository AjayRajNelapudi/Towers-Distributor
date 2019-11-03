from math import radians, degrees, sin, cos, asin, acos, sqrt
import numpy as np
from sklearn.cluster import DBSCAN

class Settlements:
    '''
    Settlements class performs DBSCAN clustering on the entire dataset of geo-coordinates
    to identify different clusters of human settlements such as cities, towns and villages
    '''
    max_distance = 0.008 # km
    min_samples = 250
    geo_cordinates = np.array([])

    def __init__(self):
        pass

    def great_circle_distance(self, pt1, pt2):
        '''
        Computes the great circle distance between pt1 an pt2

        "Not my code, don't ask me"

        :param pt1: (latitude1, longitude1)
        :param pt2: (latitude2, longitude2)
        :return: great circle distance
        '''
        earth_radius = 6371
        lat1, lon1, lat2, lon2 = pt1[0], pt1[1], pt2[0], pt2[1]

        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # print(lat1, lat2, lon1 - lon2, sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
        param = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)
        param = float("{0:.6f}".format(param))
        return earth_radius * acos(param)

    def cluster_settlements(self, geo_coordinates):
        '''
        Performs DBSCAN clustering on self.geo_coordinates
        :param geo_coordinates: geo-coordinates of all customers' locations.
        :return: dict of clusters: datapoints
        '''
        settlements = DBSCAN(
                        eps=self.max_distance,
                        min_samples=self.min_samples,
                        # metric=self.great_circle_distance
        )
        settlements.fit(geo_coordinates)

        clusters = dict()
        for cluster, datapoint in zip(settlements.labels_, geo_coordinates):
            if cluster in clusters:
                clusters[cluster].append(datapoint)
            else:
                clusters[cluster] = [datapoint]

        for cluster in clusters:
            clusters[cluster] = np.array(clusters[cluster])

        return clusters


if __name__ == "__main__":
    import random as rd

    datapoints = []

    for i in range(1000):
        datapoints.append([rd.uniform(17, 19), rd.uniform(82, 84)])

    settlements = Settlements()
    clusters = settlements.cluster_settlements(np.array(datapoints))
    print(clusters)