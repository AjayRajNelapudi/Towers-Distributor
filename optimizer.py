import logging
import numpy as np

class Optimizer:
    '''
    This class optimizes the no of towers by merging stations with less than 25 towers
    '''
    def __init__(self, min_towers=5, min_cell_site_distance=0.005):
        self.min_towers = min_towers
        self.min_cell_site_distance = min_cell_site_distance
        self.logger = logging.getLogger("optimizer")

    def optimize(self, tower_distribution):
        '''
        This is the exposed API for optimization
        :return: optimized tower_distribution
        '''
        self.logger.debug("Removing micro clusters")
        self.tower_distribution = tower_distribution
        while self.club_base_stations():
            pass

        self.relocate_base_stations()

        self.logger.debug("Micro clusters removed")
        return self.tower_distribution

    def find_nearest_base_station_key(self, base_station):
        current_key = str(base_station)
        all_base_stations = [
            (key, region['base_station'])
            for key, region in self.tower_distribution.items()
                if key != current_key
        ]

        nearest_base_station = min(
            all_base_stations,
            key = lambda each_base_station: np.linalg.norm(each_base_station[1] - base_station)
        )

        return nearest_base_station[0] # key is at 0th index

    def has_cell_sites_within_range(self, current_cell_site, exisiting_cell_sites):
        '''
        checks if the current cell site is within range of other cell sites
        :param current_cell_site: the cellsite for the current iteration
        :param exisiting_cell_sites: all the exisiting cell sites
        :return: True if cell sites found else false
        '''
        is_within_range = lambda exisiting_cell_site: np.linalg.norm(exisiting_cell_site - current_cell_site) < self.min_cell_site_distance
        any_site_within_range = max(map(is_within_range, exisiting_cell_sites))
        return any_site_within_range

    def club_base_stations(self):
        '''
        Clubs clusters with less than 25 users
        :return: None
        '''
        self.logger.debug("Applying custom optimization")
        distribution_updated = False
        keys = list(self.tower_distribution.keys())
        for key in keys:
            if key not in self.tower_distribution:
                continue

            if len(self.tower_distribution[key]['cell_sites']) >= self.min_towers:
                continue

            current_base_station = self.tower_distribution[key]
            nearest_key = self.find_nearest_base_station_key(
                self.tower_distribution[key]['base_station']
            )
            nearest_base_station = self.tower_distribution[nearest_key]
            self.tower_distribution.pop(key)
            # self.tower_distribution.pop(nearest_key)


            nearest_base_station['users'] = np.concatenate(
                (nearest_base_station['users'], current_base_station['users']),
                axis=0
            )

            for cell_site in current_base_station['cell_sites']:
                if self.has_cell_sites_within_range(cell_site, nearest_base_station['cell_sites']):
                    continue

                nearest_base_station['cell_sites'] = np.concatenate(
                    (nearest_base_station['cell_sites'], [cell_site]),
                    axis=0
                )

            distribution_updated = True
            # self.tower_distribution[nearest_key] = nearest_base_station

            self.logger.debug("Custom optimization applied")
            return distribution_updated

    def relocate_base_stations(self):
        regions = list(self.tower_distribution.values())
        for region in regions:
            key = str(region['base_station'])
            region['base_station'] = min(
                region['cell_sites'],
                key=lambda cell_site: np.linalg.norm(region['base_station'] - cell_site)
            )
            new_key = str(region['base_station'])
            self.tower_distribution[new_key] = region
            self.tower_distribution.pop(key)