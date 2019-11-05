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
        settlement_clustering = Settlements(
            max_distance=0.012, min_samples=50,
            sub_maxdistance=0.011, sub_minsamples=20
        ) # tune max_distance around 0.012 and sub_maxdistance around 0.011
        self.settlements = settlement_clustering.cluster_settlements(self.dataset)
        return self.settlements

    def perform_cellsite_clustering(self):
        cellsite_clustering = CellSites()
        self.cellsites = cellsite_clustering.distribute_cellsites(self.settlements)
        self.base_stations = cellsite_clustering.locate_base_stations()
        return self.cellsites, self.base_stations

    def save_basestations_and_cellsites(self):
        with open("basestations.csv", "w") as basestation_file:
            basestation_writer = csv.writer(basestation_file)

            for base_station in self.base_stations.values():
                basestation_writer.writerow(list(base_station))

        with open("cellsites.csv", "w") as cellsites_file:
            cellsite_writer = csv.writer(cellsites_file)

            for settlement in self.cellsites.values():
                for cellsite in settlement:
                    cellsite_writer.writerow(list(cellsite))

    def display_visuals(self):
        visuals = Visuals()
        visuals.display_towers(
            self.settlements,
            self.base_stations,
            self.cellsites
        )


if __name__ == "__main__":
    controller = Controller("dataset.csv")

    settlements = controller.perform_settlement_clustering()
    print("Settlements:", settlements.keys())

    cellsites, base_stations = controller.perform_cellsite_clustering()
    print("Cellsites count:", sum(map(len, cellsites.values())))

    controller.save_basestations_and_cellsites()
    controller.display_visuals()
