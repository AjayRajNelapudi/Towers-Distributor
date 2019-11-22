import logging
import numpy as np

class Optimizer:
    '''
    This class optimizes the no of towers by merging stations with less than 25 towers
    '''
    def __init__(self, tower_distribution):
        self.tower_distribution = tower_distribution
        self.logger = logging.getLogger("optimizer")

    def optimize(self):
        '''
        This is the exposed API for optimization
        :return: optimized tower_distribution
        '''
        self.logger.debug("Removing micro clusters")
        micro_clusters_present = lambda min_users: min([len(base_station['users'])
                                                       for base_station in self.tower_distribution.values()
                                                       ]) < min_users
        while micro_clusters_present(25):
            self.club_base_stations()

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

    def has_cell_sites_within_range(self, current_cell_site, exisiting_cell_sites, close_range):
        '''
        checks if the current cell site is within range of other cell sites
        :param current_cell_site: the cellsite for the current iteration
        :param exisiting_cell_sites: all the exisiting cell sites
        :param close_range: the distance between current cell site to all cell sites
        :return: True if cell sites found else false
        '''
        is_within_range = lambda exisiting_cell_site: np.linalg.norm(exisiting_cell_site - current_cell_site) < close_range
        return np.any(is_within_range(exisiting_cell_sites))

    def club_base_stations(self):
        '''
        Clubs clusters with less than 25 users
        :return: None
        '''
        self.logger.debug("Applying custom optimization")
        keys = list(self.tower_distribution.keys())
        for key in keys:
            if key not in self.tower_distribution:
                continue

            if len(self.tower_distribution[key]['users']) >= 25:
                continue

            current_base_station = self.tower_distribution[key]
            nearest_key = self.find_nearest_base_station_key(
                self.tower_distribution[key]['base_station']
            )
            nearest_base_station = self.tower_distribution[nearest_key]
            self.tower_distribution.pop(key)


            nearest_base_station['users'] = np.concatenate(
                (nearest_base_station['users'], current_base_station['users']),
                axis=0
            )

            for cell_site in current_base_station['cell_sites']:
                if self.has_cell_sites_within_range(cell_site, nearest_base_station['cell_sites'], 0.005):
                    continue

                nearest_base_station['cell_sites'] = np.concatenate(
                    (nearest_base_station['cell_sites'], [cell_site]), axis=0
                )

            self.logger.debug("Custom optimization applied")

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