import logging
import numpy as np
from scipy.spatial.distance import cdist

class Evaluator:
    '''
    Evaluates the number of users that fall within the range of one cell site atleast
    '''
    def __init__(self, radiation_range):
        self.radiation_range = radiation_range
        self.logger = logging.getLogger("evaluator")

    def get_users_and_cell_sites(self):
        users = np.array(
            [user for region in self.tower_distribution.values() for user in region['users']]
        )
        cell_sites = np.array(
            [cell_site for region in self.tower_distribution.values() for cell_site in region['cell_sites']]
        )

        return users, cell_sites


    def evaluate(self, tower_distribution):
        '''
        Exposed function for evaluation
        :param tower_distribution: the UBC data structure
        :return:
        '''
        self.tower_distribution = tower_distribution
        users, cell_sites = self.get_users_and_cell_sites()
        is_within_range = lambda distance: distance <= self.radiation_range
        closest_cell_site_distances = np.min(cdist(users, cell_sites, 'euclidean'), axis=1)
        users_within_range = sum(map(is_within_range, closest_cell_site_distances))

        acccuracy = users_within_range * 100 / len(users)

        self.logger.debug("Users = " + str(len(users)))
        self.logger.debug("Cell Sites = " + str(len(cell_sites)))
        self.logger.debug("Accuracy = " + str(acccuracy) + " %")

        return len(users), len(cell_sites), acccuracy

if __name__ == "__main__":
    from datahandler import *

    deserializer = Deserializer()
    deserializer.restore("tower-distribution.json")
    tower_distribution = deserializer.deserialize()

    evaluator = Evaluator(tower_distribution)
    acccuracy = evaluator.evaluate()
    print(acccuracy)
