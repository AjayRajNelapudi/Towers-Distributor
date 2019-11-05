import numpy as np

class Optimizer:
    '''
    This class optimises the cell sites but modifiying the settlements
    and including the noisy points ot avoid loss.

    Noisy points should not be excluded as these are the locations of self.users.
    '''
    def __init__(self, users, base_stations, cell_sites):
        self.users = users
        self.base_stations = base_stations
        self.cell_sites = cell_sites

    def optimize(self):
        '''
        includes -1 label to its closest points
        :return: base stations => (cellsites, self.users)
        '''
        towers_distribution = dict()
        for key in self.users.keys():
            if key < 0:
                base_station = self.find_closest_basestation(self.base_stations[key])
            else:
                base_station = self.base_stations[key]

            if base_station.tostring() in towers_distribution:
                combined_cellsites = np.concatenate(
                    (towers_distribution[base_station.tostring()]['cell_sites'], self.cell_sites[key]), axis=0
                )
                combined_users = np.concatenate(
                    (towers_distribution[base_station.tostring()]['users'], self.users[key]), axis=0
                )
                towers_distribution[base_station.tostring()] = {
                    'cell_sites': combined_cellsites,
                    'base_station': base_station,
                    'users': combined_users
                }
            else:
                towers_distribution[base_station.tostring()] = {
                    'cell_sites': self.cell_sites[key],
                    'base_station': self.base_stations[key],
                    'users': self.users[key]
                }

            # towers_distribution[self.base_stations[key].tostring()] = {
            #     'cell_sites': self.cell_sites[key],
            #     'base_station': self.base_stations[key],
            #     'users': self.users[key]
            # }
                
        return towers_distribution

    def find_closest_basestation(self, base_station):
        all_basestations = list(map(list, self.base_stations.values()))
        all_basestations.remove(list(base_station))

        closest_basestation = min(
            np.array(all_basestations),
            key=lambda each_basestation: np.linalg.norm(each_basestation - base_station)
        )

        return closest_basestation

