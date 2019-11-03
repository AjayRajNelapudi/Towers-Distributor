from addressmapper import AddressMapper
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

    def perform_cellsite_clustering(self):
        cellsite_clustering = CellSites()
        self.cellsites = cellsite_clustering.distribute_cellsites(self.settlements)

    def save_cellsites(self):
        with open("cellsites.csv") as cellsites_file:
            cellsite_writer = csv.writer(cellsites_file)

            for cellsite in self.cellsites:
                cellsite_writer.write(list(cellsite))

    def display_visuals(self):
        visuals = Visuals()
        visuals.display_towers(self.dataset, self.cellsites)


if __name__ == "__main__":
    controller = Controller("dataset.csv")
    controller.perform_settlement_clustering()
    controller.perform_cellsite_clustering()
    controller.save_cellsites()
    controller.display_visuals()
