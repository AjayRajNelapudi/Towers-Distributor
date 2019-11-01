from addressmapper import AddressMapper
from settlements import Settlements
from cellsites import CellSites
from visuals import Visuals

class Controller:
    def __init__(self, dataset_file):
        pass

    def get_all_datapoints(self):
        pass

    def perform_settlement_clustering(self):
        pass

    def perform_cellsite_clustering(self):
        pass

    def display_visuals(self):
        pass


if __name__ == "__main__":
    controller = Controller(None)
    controller.get_all_datapoints()
    controller.perform_settlement_clustering()
    controller.perform_cellsite_clustering()
    controller.display_visuals()
