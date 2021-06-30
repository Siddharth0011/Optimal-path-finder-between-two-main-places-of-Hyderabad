We have used the edges.txt dataset for our program, it contains edges existing between nodes of my map
For getting latitude and longitude we have used bing maps api
For getting distances between nodes we have used geodesic from geopy.distance
For graph we have used dictionary of lists, which works in similar way as that of adjacency list(Graph is undirected) 
g value of a starting node is set to 0
g value of subsequent nodes is addition of g value of parent and distance between parent and node
h value is distance between node and destination
Then i have called A* algorithm to get path between my source and destination
Then we plot the map using gmplot.
We also calculate the Transit time using bing maps api
