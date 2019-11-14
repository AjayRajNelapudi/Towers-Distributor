import os
import csv
import json
import logging
import logging.config
import numpy as np
from settlements import Settlements
from cellsites import CellSites
from optimizer import Optimizer
from visualizer import Visuals

class TowersDistributor:
    '''
    Towers Distributor acts as the controller for all the functions of the project
    '''
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
            },
        },
        "handlers": {
            "main": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "main.log"
            },
            "towersdistributor": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "towersdistributor.log"
            },
            "settlements": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "settlements.log"
            },
            "cellsites": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "cellsites.log"
            },
            "optimizer": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "optimizer.log"
            },
            "visualizer": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "visualizer.log"
            }
        },
        "loggers": {
            "towersdistributor": {
                "handlers": ["towersdistributor", "main"],
                "level": "DEBUG",
            },
            "settlements": {
                "handlers": ["settlements", "main"],
                "level": "DEBUG",
            },
            "cellsites": {
                "handlers": ["cellsites", "main"],
                "level": "DEBUG",
            },
            "optimizer": {
                "handlers": ["optimizer", "main"],
                "level": "DEBUG",
            },
            "visualizer": {
                "handlers": ["visualizer", "main"],
                "level": "DEBUG",
            },
        }
    }

    def __init__(self, dataset_filepath, output_JSON_file, output_html_map_file):
        logging.config.dictConfig(self.LOGGING)
        with open(dataset_filepath) as dataset_file:
            dataset_reader = csv.reader(dataset_file)
            self.dataset = np.array([list(map(float, datapoint)) for datapoint in dataset_reader])
        self.output_JSON_file = output_JSON_file
        self.output_html_map_file = output_html_map_file
        self.logger = logging.getLogger("towersdistributor")
        self.logger.debug("Towers Distributor Initialized")

    def perform_settlement_clustering(self):
        self.logger.debug("Performing Level 1 clustering")
        settlement_clustering = Settlements()
        self.settlements = settlement_clustering.cluster_settlements(self.dataset)
        self.base_stations = settlement_clustering.locate_base_stations()
        self.logger.debug("Level 1 clustering done")

    def perform_cellsite_clustering(self):
        self.logger.debug("Performing Level 2 clustering")
        cellsite_clustering = CellSites()
        self.cell_sites = cellsite_clustering.distribute_cellsites(self.settlements)
        # raise SystemExit("60 % execution done") # My college measures code written as % of unknown total code
        self.logger.debug("Level 2 clustering done")

    def format(self):
        self.logger.debug("Formatting to dictionary")
        self.tower_distribution = dict()
        for key in self.settlements.keys():
            self.tower_distribution[self.base_stations[key].tostring()] = {
                'cell_sites': self.cell_sites[key],
                'base_station': self.base_stations[key],
                'users': self.settlements[key]
            }
        self.logger.debug("UBC dictionary formatted")

    def optimize(self):
        self.logger.debug("Performing UBC optimization")
        ubc_optimizer = Optimizer(self.tower_distribution.copy())
        self.tower_distribution = ubc_optimizer.optimize()
        self.logger.debug("UBC optimization done")

    def save_tower_distribution(self):
        self.logger.debug("Saving UBC dict to JSON")
        tower_distribution = dict()
        keys = list(self.tower_distribution.keys())
        for key in keys:
            base_station = self.tower_distribution[key].copy()

            base_station['users'] = str(base_station['users'])
            base_station['base_station'] = str(base_station['base_station'])
            base_station['cell_sites'] = str(base_station['cell_sites'])

            tower_distribution[str(key)] = base_station

        tower_distribution = json.dumps(tower_distribution)
        with open(self.output_JSON_file, "w") as tower_distribution_file:
            tower_distribution_file.write(tower_distribution)

        self.logger.debug("UBC dictionary saved to JSON")

    def display_visuals(self):
        self.logger.debug("Creating Visuals")
        visuals = Visuals(self.tower_distribution)
        # visuals.display_distribution()
        visuals.make_map(self.output_html_map_file)
        self.logger.debug("Visuals created")

        self.logger.debug("Calling default browser to open map")
        os.system("open " + self.output_html_map_file)


if __name__ == "__main__":
    distributor = TowersDistributor("dataset.csv", "tower-distribution.json", "tower-distribution.html")

    distributor.perform_settlement_clustering()
    distributor.perform_cellsite_clustering()

    distributor.format()
    distributor.optimize()

    distributor.save_tower_distribution()
    distributor.display_visuals()

    print("Tower Distribution serialized to tower_distribution.json")
    print("Open map.html to visualize on map")
