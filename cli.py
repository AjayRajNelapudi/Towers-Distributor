import click
from towersdistributor import TowersDistributor

@click.command()
@click.argument("dataset", nargs=1, required=True)
@click.argument("output_json_file", nargs=1, required=True)
@click.argument("output_map_html_file", nargs=1, required=True)
@click.option("-rr", "--radiation_range", default=1000, help="radiation range of cell site(in metres)")
@click.option("-mt", "--min_towers", default=5, help="minimum towers to be considered as a region")
@click.option("-mg", "--min_gap", default=400, help="minimum distance between towers(in metres) to not be clubbed")
@click.option("-l/-dl", "--log/--disable_logs", default=True, help="To disable logging the execution")
def distribute_towers(dataset, output_json_file, output_map_html_file, radiation_range, min_towers, min_gap, log):
    '''
    Distributes 5G cell sites and base stations using Spectral & K-Means clustering.
    Further enhanced using custom optimization techniques.
    '''
    if radiation_range < 0:
        raise ValueError("radiation range cannot be negative")
    if min_towers < 0:
        raise ValueError("min no of towers per cluster cannot be negative")
    if min_gap < 0:
        raise ValueError("min gap between cell sites cannot be negative")

    distributor = TowersDistributor(dataset, enable_logger=log)

    distributor.perform_settlement_clustering()
    distributor.perform_cellsite_clustering(radiation_range=radiation_range)

    distributor.format()
    distributor.optimize(min_towers=min_towers, min_cell_site_distance=min_gap)

    distributor.serialize_and_save_data(output_json_file)
    distributor.make_and_display_map(output_map_html_file)

    # distributor.evaluate()

if __name__ == "__main__":
    distribute_towers()