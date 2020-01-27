import folium
import logging
import itertools
import numpy as np
import matplotlib.pyplot as plt

class Visuals:
    '''
    Displays the map, users and the cell sites predicted
    '''
    colors = itertools.cycle([
        '#e6194b', '#3cb44b', '#ffe119', '#4363d8',
        '#f58231', '#46f0f0', '#f032e6', '#bcf60c',
        '#fabebe', '#008080', '#e6beff', '#9a6324',
        '#fffac8', '#800000', '#aaffc3', '#808000',
        '#000075', '#808080', '#ffd8b1', '#ffffff',
        '#000000'
    ])


    def __init__(self, tower_distribution):
        self.tower_distribution = tower_distribution
        self.logger = logging.getLogger("visualizer")

    def display_distribution(self):
        '''
        Displays the users and cell sites
        :return: None
        '''

        # users, basestations, cellsites
        for UBC in self.tower_distribution.values():
            users = UBC['users']
            base_station = UBC['base_station']
            cell_sites = UBC['cell_sites']
            color = next(self.colors)

            users_X, users_Y = zip(*users)
            plt.scatter(users_X, users_Y, c=color, marker=".")

            plt.plot(
                base_station[0], base_station[1],
                c=color, marker="p", markersize=12, markeredgecolor="black"
            )


            for cellsites_X, cellsites_Y in cell_sites:
                plt.plot(
                    cellsites_X, cellsites_Y,
                    c=color, marker="^", markersize=10, markeredgecolor="black"
                )

        # plt.savefig("tower-distribution.png", dpi=300)
        plt.show()

    # def display_towers(self, towers_distribution):
    #     for settlement in towers_distribution.values():
    #         users = settlement['users']
    #         base_station = settlement['base_station']
    #         cell_sites = settlement['cell_sites']
    #
    #         users_X, users_Y = zip(*users)
    #         plt.scatter(users_X, users_Y, marker='.', c='lightgreen', label='users')
    #
    #         plt.scatter(base_station[0], base_station[1], marker='p', c='blue', label='base stations')
    #
    #         cellsites_X, cellsites_Y = zip(*cell_sites)
    #         plt.scatter(cellsites_X, cellsites_Y, marker='^', c='red', label='cell sites')

    # plt.show()

    def make_map(self, save_path):
        '''
        This function uses folium to create a distribution map
        :param save_path: Path to save the map
        :return: None
        '''
        self.logger.debug("Making map with cellsite distribution")
        map = folium.Map(
            location=[17.777612, 83.250768],
            titles="OpenStreetMap",
            zoom_start=12
        )

        for region in self.tower_distribution.values():
            users = region['users']
            base_station = region['base_station']
            cell_sites = region['cell_sites']
            color = next(self.colors)

            for user in users:
                user_marker = folium.Circle(
                    location=user,
                    radius=0.25,
                    color=color,
                    fill=True,
                    fill_color=color,
                    tooltip="user"
                )
                map.add_child(user_marker)

            for cell_site in cell_sites:
                cell_site_marker = folium.Marker(
                    location=cell_site,
                    icon=folium.Icon(icon="tower", color="darkblue")
                )
                map.add_child(cell_site_marker)

                cell_site_circle = folium.Circle(
                    location=cell_site,
                    radius=800,
                    color=color,
                    fill=True,
                    tooltip="Cellsite"
                )
                map.add_child(cell_site_circle)

                backhaul_line = folium.ColorLine(
                    positions=(base_station, cell_site),
                    colors=[0],
                    colormap=[color, "black"],
                    weight=2,
                    tooltip="Backhaul"
                )
                map.add_child(backhaul_line)

            base_station_marker = folium.Marker(
                location=base_station,
                icon=folium.Icon(icon="home", color="orange")
            )
            map.add_child(base_station_marker)

        map.save(save_path)

if __name__ == "__main__":
    import os
    from datahandler import *

    deserializer = Deserializer()
    deserializer.restore("outputs/td.json")
    tower_distribution = deserializer.deserialize()

    visuals = Visuals(tower_distribution)
    visuals.make_map("tower-distribution.html")
    os.system("open tower-distribution.html")