import os
import csv
import json
import logging
import logging.config
import numpy as np
from regions import Regions
from cellsites import CellSites
from optimizer import Optimizer
from visualizer import Visuals
from datahandler import *
from evaluator import Evaluator

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
                "filename": "logs/main.log"
            },
            "towersdistributor": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "logs/towersdistributor.log"
            },
            "regions": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "logs/regions.log"
            },
            "cellsites": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "logs/cellsites.log"
            },
            "optimizer": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "logs/optimizer.log"
            },
            "visualizer": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "logs/visualizer.log"
            },
            "evaluator": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "logs/evaluator.log"
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "towersdistributor": {
                "handlers": ["towersdistributor", "main", "console"],
                "level": "DEBUG",
            },
            "regions": {
                "handlers": ["regions", "main", "console"],
                "level": "DEBUG",
            },
            "cellsites": {
                "handlers": ["cellsites", "main", "console"],
                "level": "DEBUG",
            },
            "optimizer": {
                "handlers": ["optimizer", "main", "console"],
                "level": "DEBUG",
            },
            "visualizer": {
                "handlers": ["visualizer", "main", "console"],
                "level": "DEBUG",
            },
            "evaluator": {
                "handlers": ["evaluator", "main", "console"],
                "level": "DEBUG",
            }
        }
    }

    def __init__(self, dataset_filepath, enable_logger=True):
        if enable_logger:
            if "logs" not in os.listdir(os.getcwd()):
                os.mkdir("logs")
            logging.config.dictConfig(self.LOGGING)

        with open(dataset_filepath) as dataset_file:
            dataset_reader = csv.reader(dataset_file)
            self.dataset = np.array([list(map(float, datapoint)) for datapoint in dataset_reader])

        self.logger = logging.getLogger("towersdistributor")
        self.logger.debug("Towers Distributor Initialized")

    def metres_to_geodistance(self, metres):
        if metres < 0:
            raise ValueError("distance cannot be negative")
        geo_distance = metres / (10 ** 5)
        return geo_distance

    def perform_settlement_clustering(self):
        self.logger.debug("Performing Level 1 clustering")

        settlement_clustering = Regions()
        self.regions = settlement_clustering.detect_regions(self.dataset)
        self.base_stations = settlement_clustering.locate_base_stations_proximity()

        self.logger.debug("Level 1 clustering done")

    def perform_cellsite_clustering(self, radiation_range=1000):
        if radiation_range < 0:
            raise ValueError("radiation range cannot be negative")

        self.radiation_range = self.metres_to_geodistance(radiation_range)
        self.logger.debug("Performing Level 2 clustering")

        cellsite_clustering = CellSites(radiation_range=self.radiation_range)
        self.cell_sites = cellsite_clustering.distribute_cellsites(self.regions)

        self.logger.debug("Level 2 clustering done")

    def format(self):
        self.logger.debug("Formatting to dictionary")

        self.tower_distribution = {}
        for key in self.regions.keys():
            self.tower_distribution[str(self.base_stations[key])] = {
                'cell_sites': self.cell_sites[key],
                'base_station': self.base_stations[key],
                'users': self.regions[key]
            }

        self.logger.debug("Regions dictionary formatted")

    def optimize(self, min_towers=5, min_cell_site_distance=500):
        if min_towers < 0:
            raise ValueError("min no of towers per cluster cannot be negative")
        if min_cell_site_distance < 0:
            raise ValueError("min gap between cell sites cannot be negative")

        self.min_towers = min_towers
        self.min_cell_site_distance = self.metres_to_geodistance(min_cell_site_distance)
        self.logger.debug("Performing Region optimization")

        region = Optimizer(min_towers=self.min_towers, min_cell_site_distance=self.min_cell_site_distance)
        self.tower_distribution = region.optimize(self.tower_distribution)

        self.logger.debug("UBC optimization done")

    def serialize_and_save_data(self, output_JSON_file):
        self.output_JSON_file = output_JSON_file
        self.logger.debug("Saving UBC dict to JSON")
        serializer = Serializer(self.tower_distribution)
        serializer.serialize()
        serializer.save(self.output_JSON_file)
        self.logger.debug("UBC dictionary saved to JSON")

    def make_and_display_map(self, output_map_html_file):
        self.output_html_map_file = output_map_html_file
        self.logger.debug("Creating Visuals")
        visuals = Visuals(self.tower_distribution)
        # visuals.display_distribution()
        visuals.make_map(self.output_html_map_file)
        self.logger.debug("Visuals created")

        self.logger.debug("Calling default browser to open map")
        os.system("open " + self.output_html_map_file)

    def evaluate(self):
        self.logger.debug("Evaluating model")

        accuracy_evaluator = Evaluator(radiation_range=self.radiation_range)
        users, cell_site_count, accuracy = accuracy_evaluator.evaluate(tower_distribution=self.tower_distribution)

        self.logger.debug("Model evaluated")


if __name__ == "__main__":
    distributor = TowersDistributor("datasets/custom-dataset.csv", enable_logger=True)

    distributor.perform_settlement_clustering()
    distributor.perform_cellsite_clustering()

    distributor.format()
    distributor.optimize()

    distributor.serialize_and_save_data("outputs/custom-td.json")
    distributor.make_and_display_map("maps/custom-td.html")

    distributor.evaluate()

# 1010, 15
# 1500, 25
# 2000, 50
# 4000, 85
# 4500, 128
# 5184, 173

# 10000, 318
# 100000, 3404
# 1000000, 34720