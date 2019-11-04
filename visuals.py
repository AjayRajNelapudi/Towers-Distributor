import numpy as np
import matplotlib.pyplot as plt

class Visuals:
    '''
    Displays the map, users and the cell sites predicted
    '''
    def __init__(self):
        pass

    def display_towers(self, users, base_stations, towers):
        '''
        Displays the users and cell sites
        :return: None
        '''
        users_X = np.array([user[0] for user in users])
        users_Y = np.array([user[1] for user in users])
        plt.scatter(users_X, users_Y, c='lightgreen', marker='.', label='users')

        base_stations_X = np.array([base_station[0] for base_station in base_stations])
        base_stations_Y = np.array([base_station[1] for base_station in base_stations])
        plt.scatter(base_stations_X, base_stations_Y, c='blue', marker='p', label='base stations')

        for settlement in towers:
            towers_X = np.array([tower[0] for tower in settlement])
            towers_Y = np.array([tower[1] for tower in settlement])
            plt.scatter(towers_X, towers_Y, c='red', marker='^', label='cell sites')
        # plt.scatter(towers_X, towers_Y, s=800, facecolors='none', edgecolors='r')

        # plt.legend()
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