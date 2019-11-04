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
        settlement_clustering = Settlements(max_distance=0.012, min_samples=50)
        self.settlements = settlement_clustering.cluster_settlements(self.dataset)
        return self.settlements

    def perform_cellsite_clustering(self):
        cellsite_clustering = CellSites()
        self.cellsites = cellsite_clustering.distribute_cellsites(self.settlements)
        return self.cellsites

    def save_cellsites(self):
        with open("cellsites.csv", "w") as cellsites_file:
            cellsite_writer = csv.writer(cellsites_file)

            for cellsite in self.cellsites:
                cellsite_writer.writerow(list(cellsite))

    def display_visuals(self):
        visuals = Visuals()
        visuals.display_towers(self.dataset, self.cellsites)


if __name__ == "__main__":
    controller = Controller("dataset.csv")

    settlements = controller.perform_settlement_clustering()
    print("Settlements:", settlements.keys())

    cellsites = controller.perform_cellsite_clustering()
    print("Cellsites count:", len(cellsites))

    controller.save_cellsites()
    controller.display_visuals()

