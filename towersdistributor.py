import os
import csv
import json
import logging
import numpy as np
from settlements import Settlements
from cellsites import CellSites
from optimizer import Optimizer
from visualizer import Visuals

class TowersDistributor:
    def __init__(self, dataset_filepath, output_file):
        with open(dataset_filepath) as dataset_file:
            dataset_reader = csv.reader(dataset_file)
            self.dataset = np.array([list(map(float, datapoint)) for datapoint in dataset_reader])
        self.output_file = output_file
        self.logger = logging.getLogger("towersdistributor")

    def perform_settlement_clustering(self):
        settlement_clustering = Settlements()
        self.settlements = settlement_clustering.cluster_settlements(self.dataset)
        self.base_stations = settlement_clustering.locate_base_stations()

    def perform_cellsite_clustering(self):
        cellsite_clustering = CellSites()
        self.cell_sites = cellsite_clustering.distribute_cellsites(self.settlements)
        # raise SystemExit("60 % execution done") # My college measures code written as % of unknown total code

    def format(self):
        self.tower_distribution = dict()
        for key in self.settlements.keys():
            self.tower_distribution[self.base_stations[key].tostring()] = {
                'cell_sites': self.cell_sites[key],
                'base_station': self.base_stations[key],
                'users': self.settlements[key]
            }

    def optimize(self):
        ubc_optimizer = Optimizer(self.tower_distribution.copy())
        self.tower_distribution = ubc_optimizer.optimize()

    def save_tower_distribution(self):
        tower_distribution = dict()
        keys = list(self.tower_distribution.keys())
        for key in keys:
            base_station = self.tower_distribution[key].copy()

            base_station['users'] = str(base_station['users'])
            base_station['base_station'] = str(base_station['base_station'])
            base_station['cell_sites'] = str(base_station['cell_sites'])

            tower_distribution[str(key)] = base_station

        tower_distribution = json.dumps(tower_distribution)
        with open(self.output_file, "w") as tower_distribution_file:
            tower_distribution_file.write(tower_distribution)

    def display_visuals(self):
        visuals = Visuals(self.tower_distribution)
        # visuals.display_distribution()
        visuals.make_map("map.html")
        os.system("open map.html")


if __name__ == "__main__":
    distributor = TowersDistributor("dataset.csv", "tower-distribution.json")

    distributor.perform_settlement_clustering()
    distributor.perform_cellsite_clustering()

    distributor.format()
    distributor.optimize()

    distributor.save_tower_distribution()
    distributor.display_visuals()

    print("Tower Distribution serialized to tower_distribution.json")
    print("Open map.html to visualize on map")