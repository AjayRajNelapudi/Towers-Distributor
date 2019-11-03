import numpy as np
import matplotlib.pyplot as plt

class Visuals:
    '''
    Displays the map, users and the cell sites predicted
    '''
    def display_towers(self, users, towers):
        '''
        Displays the users and cell sites
        :return: None
        '''
        users_X = np.array([user[0] for user in users])
        users_Y = np.array([user[1] for user in users])
        plt.scatter(users_X, users_Y, c='lightblue', marker='.')

        towers_X = np.array([tower[0] for tower in towers])
        towers_Y = np.array([tower[1] for tower in towers])
        plt.scatter(towers_X, towers_Y, c='red', marker='^')

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