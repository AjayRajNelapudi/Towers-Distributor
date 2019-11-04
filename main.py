from settlements import Settlements
from cellsites import CellSites
from visuals import Visuals
import csv
import numpy as np
import statistics

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

    def locate_base_stations(self):
        base_stations = []
        for label, cellsites in self.cellsites.items():
            base_station_location = [
                statistics.mean([cellsite[0] for cellsite in cellsites]),
                statistics.mean([cellsite[1] for cellsite in cellsites])
            ]
            base_stations.append(base_station_location)

        self.base_stations = np.array(base_stations)

    def save_basestations_and_cellsites(self):
        with open("basestations.csv", "w") as basestation_file:
            basestation_writer = csv.writer(basestation_file)

            for base_station in self.base_stations:
                basestation_writer.writerow(list(base_station))

        with open("cellsites.csv", "w") as cellsites_file:
            cellsite_writer = csv.writer(cellsites_file)

            for settlement in self.cellsites.values():
                for cellsite in settlement:
                    cellsite_writer.writerow(list(cellsite))

    def display_visuals(self):
        visuals = Visuals()
        visuals.display_towers(
            self.dataset,
            self.base_stations,
            self.cellsites.values()
        )


if __name__ == "__main__":
    controller = Controller("dataset.csv")

    settlements = controller.perform_settlement_clustering()
    print("Settlements:", settlements.keys())

    cellsites = controller.perform_cellsite_clustering()
    print("Cellsites count:", sum(map(len, cellsites.values())))

    controller.locate_base_stations()

    controller.save_basestations_and_cellsites()
    controller.display_visuals()

