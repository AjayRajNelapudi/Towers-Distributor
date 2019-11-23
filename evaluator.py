import json
import logging
import numpy as np

class Evaluator:
    cell_site_range = 0.008

    def __init__(self, filename):
        with open(filename) as file:
            tower_distribution = json.load(file)

        self.tower_distribution = dict()
        for key, region in tower_distribution.items():

            users = np.array(
                [
                    np.fromstring(
                        user.replace("[", "").replace("]", ""),
                        dtype=np.float,
                        sep=" "
                    )
                    for user in region['users'].split("\n")
                ]
            )

            cell_sites = np.array(
                [
                    np.fromstring(
                        user.replace("[", "").replace("]", ""),
                        dtype=np.float,
                        sep=" "
                    )
                    for user in region['cell_sites'].split("\n")
                ]
            )

            self.tower_distribution[key] = {
                'users': users,
                'cell_sites': cell_sites,
            }

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

        within_range_count = 0
        for user in users:
            min_tower_distance = min([np.linalg.norm(user - cell_site) for cell_site in cell_sites])
            if min_tower_distance > self.cell_site_range:
                continue

            within_range_count += 1

        acccuracy = within_range_count / len(users)

        self.logger.debug("Users = " + str(len(users)))
        self.logger.debug("Cell Sites = " + str(len(cell_sites)))
        self.logger.debug("Accuracy = " + str(acccuracy))

        return len(users), len(cell_sites), acccuracy

if __name__ == "__main__":
    evaluator = Evaluator("tower-distribution.json")
    acccuracy = evaluator.evaluate()
    print(acccuracy)
