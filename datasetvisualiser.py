import csv
import folium
import numpy as np

dataset_filepath = "/users/ajayraj/documents/towersdistributor/hotspots.csv"
with open(dataset_filepath) as dataset_file:
    dataset_reader = csv.reader(dataset_file)
    dataset = np.array([list(map(float, datapoint)) for datapoint in dataset_reader])

map = folium.Map(location=np.array([17.777612, 83.250768]), titles='OpenStreetMap')
for datapoint in dataset:
    folium.Circle(
        location=datapoint,
        radius=1,
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(map)
map.save("/users/ajayraj/documents/towers-distributor/hotspots.html")