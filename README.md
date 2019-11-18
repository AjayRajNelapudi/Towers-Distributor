# Towers-Distributor
Distributes 5G cell sites and base stations using Spectral clustering, K-Means clustering and custom optimization techniques.

[Output Map Hyperlink](https://towersdistributor.000webhostapp.com/)

<br>
Each color represents a cluster with a single base station<br>
The dots represent the users<br>
The pentagons represent the base stations<br>
The triangles represent the cell sites<br>
<br>

<b>Steps Followed</b><br>
1. Build affinity matrix.<br>
2. Compute Eigen decompostiion for finding optimal no of clusters.<br>
3. Apply spectral clustering.<br>
4. For each cluster find proper k value.<br>
5. Use K-Means to cluster each of the spectral cluster and find centroids for cell sites.<br>
6. Apply custom optimization techniques to reduce base station and cell site count.<br>
7. Plot on matplotlib.<br>
8. Serialize the data structure and write to tower_distribution.json.<br>