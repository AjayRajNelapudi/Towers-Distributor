from settlements import Settlements
from cellsites import CellSites
from visuals import Visuals
import csv
import numpy as np

class Controller:
    def __init__(self, dataset_filepath):
        with open(dataset_filepath) as dataset_file:
            dataset_reader = csv.reader(dataset_file)
            self.dataset = np.array([list(map(float, datapoint)) for datapoint in dataset_reader])

    def perform_settlement_clustering(self):
        settlement_clustering = Settlements()
        self.settlements = settlement_clustering.cluster_settlements(self.dataset)
        self.base_stations = settlement_clustering.locate_base_stations()
        return self.settlements

    def perform_cellsite_clustering(self):
        cellsite_clustering = CellSites()
        self.cell_sites = cellsite_clustering.distribute_cellsites(self.settlements)
        return self.cell_sites

    def format(self):
        self.towers_distribution = dict()
        for key in self.settlements.keys():
            self.towers_distribution[self.base_stations[key].tostring()] = {
                'cell_sites': self.cell_sites[key],
                'base_station': self.base_stations[key],
                'users': self.settlements[key]
            }
        return self.towers_distribution

    def save_basestations_and_cellsites(self):
        with open("basestations.csv", "w") as basestation_file:
            basestation_writer = csv.writer(basestation_file)

            for base_station in self.base_stations.values():
                basestation_writer.writerow(list(base_station))

        with open("cellsites.csv", "w") as cellsites_file:
            cellsite_writer = csv.writer(cellsites_file)

            for settlement in self.cell_sites.values():
                for cellsite in settlement:
                    cellsite_writer.writerow(list(cellsite))

    def display_visuals(self):
        visuals = Visuals()
        visuals.display_towers(self.towers_distribution)


if __name__ == "__main__":
    controller = Controller("dataset.csv")

    settlements = controller.perform_settlement_clustering()
    print("Base Stations Count:", len(settlements.keys()))

    cellsites = controller.perform_cellsite_clustering()
    print("Cellsites count:", sum(map(len, cellsites.values())))

    controller.format()

    controller.save_basestations_and_cellsites()
    controller.display_visuals()
