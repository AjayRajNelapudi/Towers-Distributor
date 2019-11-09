import folium
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
        map = folium.Map(location=[17.777612, 83.250768], titles='OpenStreetMap', zoom_start=11)
        for UBC in self.tower_distribution.values():
            users = UBC['users']
            base_station = UBC['base_station']
            cell_sites = UBC['cell_sites']
            color = next(self.colors)

            base_station_marker = folium.Circle(
                location=base_station,
                radius=1,
                color=color,
                fill=True,
                fill_color=color
            )
            map.add_child(base_station_marker)

            for cell_site in cell_sites:
                cell_site_marker = folium.Marker(
                    location=cell_site,
                )
                map.add_child(cell_site_marker)

                backhaul_line = folium.ColorLine(
                    positions=(base_station, cell_site),
                    colors=[0],
                    colormap=[color, 'black'],
                    weight=4
                )
                map.add_child(backhaul_line)

        map.save(save_path)
