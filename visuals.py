import itertools
import numpy as np
import matplotlib.pyplot as plt

class Visuals:
    '''
    Displays the map, users and the cell sites predicted
    '''
    def __init__(self):
        pass

    def display_towers(self, users_regions, basestation_regions, cellsites_regions):
        '''
        Displays the users and cell sites
        :return: None
        '''
        colors = itertools.cycle([
            '#CDBD7E',
            '#A4D47A',
            '#7AD4C9',
            '#7C9289',
            '#F196E0',
            '#C1F196',
            '#7AB3D4',
            '#7A84D4',
            '#947AD4',
            '#CC7AD4',
            '#D47A98',
        ])

        # users, basestations, cellsites
        UBC = zip(
            users_regions.values(), basestation_regions.values(), cellsites_regions.values()
        )
        for users, base_station, cell_sites in UBC:
            color = next(colors)

            users_X, users_Y = zip(*users)
            plt.scatter(users_X, users_Y, c=color, marker='.')

            plt.plot(
                base_station[0], base_station[1],
                c=color, marker='p', markersize=10, markeredgecolor='red'
            )

            # cellsites_X, cellsites_Y = zip(*cell_sites)
            # plt.scatter(cellsites_X, cellsites_Y, c=color, marker='^', markeredgecolor='red')

            for cellsites_X, cellsites_Y in cell_sites:
                plt.plot(
                    cellsites_X, cellsites_Y,
                    c=color, marker='^', markersize=10, markeredgecolor='red'
                )

        plt.show()

    def get_map(self):
        pass


if __name__ == "__main__":
    user_count = 500
    X = np.random.rand(user_count)
    Y = np.random.rand(user_count)
    users = np.array([[x, y] for x, y in zip(X, Y)])

    X = np.random.rand(20)
    Y = np.random.rand(20)
    towers = np.array([[x, y] for x, y in zip(X, Y)])

    visuals = Visuals()
    visuals.display_towers(users, towers)

# gmplot