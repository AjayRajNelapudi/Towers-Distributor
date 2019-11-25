import logging
import numpy as np
from scipy.spatial.distance import cdist

class Evaluator:
    cell_site_range = 0.08

    def __init__(self, tower_distribution):
        self.tower_distribution = tower_distribution
        self.logger = logging.getLogger("evaluator")

    def get_users_and_cell_sites(self):
        users = np.array(
            [user for region in self.tower_distribution.values() for user in region['users']]
        )
        cell_sites = np.array(
            [cell_site for region in self.tower_distribution.values() for cell_site in region['cell_sites']]
        )

        return users, cell_sites


    def evaluate(self):
        users, cell_sites = self.get_users_and_cell_sites()
        is_within_range = lambda distance: distance < self.cell_site_range
        closest_cell_site_distances = np.min(cdist(users, cell_sites, 'euclidean'), axis=1)
        users_within_range = sum(map(is_within_range, closest_cell_site_distances))

        acccuracy = users_within_range / len(users)

        self.logger.debug("Users = " + str(len(users)))
        self.logger.debug("Cell Sites = " + str(len(cell_sites)))
        self.logger.debug("Accuracy = " + str(acccuracy))

        return len(users), len(cell_sites), acccuracy

if __name__ == "__main__":
    evaluator = Evaluator("custom-td.json")
    acccuracy = evaluator.evaluate()
    print(acccuracy)
