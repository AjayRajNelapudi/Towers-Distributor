import click
from towersdistributor import TowersDistributor

@click.command()
@click.argument("dataset", nargs=1, required=True)
@click.argument("output_JSON_file", nargs=1, required=True)
@click.argument("output_map_file", nargs=1, required=True)
def distribute_towers(dataset, output_JSON_file, output_map_file):
    distributor = TowersDistributor(dataset, output_JSON_file, output_map_file)

    distributor.perform_settlement_clustering()
    distributor.perform_cellsite_clustering()

    distributor.format()
    distributor.optimize()

    distributor.save_tower_distribution()
    distributor.display_visuals()

if __name__ == "__main__":
    distribute_towers()