import itertools
import numpy as np
import matplotlib.pyplot as plt

class Visuals:
    '''
    Displays the map, users and the cell sites predicted
    '''
    def __init__(self):
        pass

    def display_towers(self, tower_distribution):
        '''
        Displays the users and cell sites
        :return: None
        '''
        colors = itertools.cycle([
            '#e6194b', '#3cb44b', '#ffe119', '#4363d8',
            '#f58231', '#46f0f0', '#f032e6',
            '#bcf60c', '#fabebe', '#008080', '#e6beff'
            '#9a6324', '#fffac8', '#800000', '#aaffc3'
            '#808000', '#000075', '#808080', '#ffd8b1'
            '#ffffff', '#000000'
        ])

        # users, basestations, cellsites
        for UBC in tower_distribution.values():
            users = UBC['users']
            base_station = UBC['base_station']
            cell_sites = UBC['cell_sites']
            color = next(colors)

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

    def get_map(self):
        pass
