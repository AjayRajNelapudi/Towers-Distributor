import csv
import numpy as np
import matplotlib.pyplot as plt

def read_hotspots(hotspots_filepath):
    with open(hotspots_filepath) as hotspots_datafile:
        datapoint_reader = csv.reader(hotspots_datafile)
        hotspots = [list(map(float, datapoint)) for datapoint in datapoint_reader]

    return hotspots

def generate_dataset(hotspots):
    users_distance = (-200, 200)
    dataset = []
    for hotspot in hotspots:
        customer_per_hotspot = np.random.randint(100, 200)
        for customer in range(customer_per_hotspot):
            x = hotspot[0] + (0.0001 * np.random.randint(*users_distance))
            y = hotspot[1] + (0.0001 * np.random.randint(*users_distance))
            dataset.append([x, y])

    return dataset

def write_dataset(dataset, dataset_filepath):
    with open(dataset_filepath, "w") as users_datafile:
        datapoint_writer = csv.writer(users_datafile, delimiter=",")
        for datapoint in dataset:
            datapoint_writer.writerow(datapoint)

def visualise_dataset(dataset):
    X = np.array([datapoint[0] for datapoint in dataset])
    Y = np.array([datapoint[1] for datapoint in dataset])
    plt.scatter(X, Y, marker=".")
    plt.show()

if __name__ == "__main__":
    hotspots = read_hotspots("hotspots.csv")
    dataset = generate_dataset(hotspots)
    write_dataset(dataset, "dataset.csv")
    visualise_dataset(dataset)