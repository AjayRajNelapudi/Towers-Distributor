import numpy as np

class Optimizer:
    '''
    This class optimizes the no of towers by merging stations with less than 25 towers
    '''
    def __init__(self, tower_distribution):
        import os
        if os.name == "nt":
            raise OSError("Windows does not support optimization.\nPlease use Linux or MacOS")
        self.tower_distribution = tower_distribution

    def optimize(self):
        print("Running Optimization Metric...")
        while min([len(base_station['users']) for base_station in self.tower_distribution.values()]) < 25:
            self.optimization_metric()

    def optimization_metric(self):
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
            self.tower_distribution.pop(nearest_key)


            nearest_base_station['users'] = np.concatenate(
                (nearest_base_station['users'], current_base_station['users']), axis=0
            )
            nearest_base_station['cell_sites'] = np.concatenate(
                (nearest_base_station['cell_sites'], current_base_station['cell_sites']), axis=0
            )
            nearest_base_station['base_station'] = np.array([
                np.mean([
                    nearest_base_station['base_station'][0],
                    current_base_station['base_station'][0]
                ]),
                np.mean([
                    nearest_base_station['base_station'][1],
                    current_base_station['base_station'][1]
                ])
            ])

            new_key = nearest_base_station['base_station'].tostring()
            self.tower_distribution[new_key] = nearest_base_station

    def find_nearest_base_station_key(self, base_station):
        current_key = base_station.tostring()
        all_base_stations = [
            (key, value['base_station'])
            for key, value in self.tower_distribution.items()
                if key != current_key
        ]

        nearest_base_station = min(
            all_base_stations,
            key = lambda each_base_station: np.linalg.norm(each_base_station[1] - base_station)
        )

        return nearest_base_station[0] # key is at 0th index