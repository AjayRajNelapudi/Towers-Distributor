import click
import logging
import logging.config
from towersdistributor import TowersDistributor

def configure_logger():
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

    logging.config.dictConfig(LOGGING)


@click.command()
@click.argument("source", nargs=1)
@click.argument("destination", nargs=1)
def distribute_towers(source, destination):
    distributor = TowersDistributor(source, destination)

    distributor.perform_settlement_clustering()
    distributor.perform_cellsite_clustering()

    distributor.format()
    distributor.optimize()

    distributor.save_tower_distribution()
    distributor.display_visuals()

    print("Tower Distribution serialized to tower_distribution.json")
    print("Open map.html to visualize on map")

if __name__ == "__main__":
    configure_logger()
    distribute_towers()