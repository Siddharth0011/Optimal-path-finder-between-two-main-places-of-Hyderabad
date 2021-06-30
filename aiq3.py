import geocoder
from geopy.distance import geodesic
import gmplot
from math import radians, cos, sin, asin, sqrt
import urllib.parse
import requests
import json
import configparser
import gmplot
import urllib.parse
import configparser
import json as JSON
import pickle
import shutil
import re


# Function to get latitude and longitude of our location using BING API
def geoloc(item):
    #sendurl = 'http://dev.virtualearth.net/REST/v1/Locations?query=' + item + '&key=' + 'fr74KQ8elKnmbJvSb2WR~vrsOlMr-SitXk-Xrhpg9ew~Al8rE9GvYa93aY_Mp9nhWAALqXXgji7pALDUt6pn0IGbl-enG0-vGIevZcCui3er'
    #Aq0cW519uOhs74Y9ncOrtlqz-QlB_3rVeL6O9a8PI-fhgyDCWipKROfV5ROtXoXI
    sendurl = 'http://dev.virtualearth.net/REST/v1/Locations?query=' + item + '&key=' + 'Aq0cW519uOhs74Y9ncOrtlqz-QlB_3rVeL6O9a8PI-fhgyDCWipKROfV5ROtXoXI'
    r = requests.get(sendurl)
    try:
        j = json.loads(r.text)
        try:
            loc = j['resourceSets'][0]['resources'][0]['geocodePoints'][0]['coordinates']
            return (tuple(loc))
        except ValueError:
            print("Wrong")
    except ValueError:
        print("Wrong")
    return []


# ******Getting lat and long for the nodes*******#
file2 = open('edges.txt', 'r')

edges = []  # stores the edges present in our map

for each in file2:
    each = str(each)
    each = each.lower()
    each = each.split('\t')
    edges.append(each)
for i in range(0, len(edges)):
    edges[i][1] = edges[i][1][0:len(edges[i][1]) - 1]

nodes1 = []  # stores the nodes present in our map
for i in range(0, len(edges)):
    a = edges[i][0]
    b = edges[i][1]
    if a not in nodes1:
        nodes1.append(a)
    if b not in nodes1:
        nodes1.append(b)

lat = {}  # stores the latitude of our nodes present in map
lng = {}  # stores the longitude of nodes present in our map
for i in range(0, len(nodes1)):
    r = geoloc(nodes1[i])
    # print(r)
    lat[nodes1[i]] = r[0]
    lng[nodes1[i]] = r[1]

# *****Creating Distance matrix for nodes*****#

dist = {}  # stores the distance between any two nodes in our map
for i in range(0, len(nodes1)):
    dist[nodes1[i]] = {}
for i in range(0, len(nodes1)):
    first_elm = (lat[nodes1[i]], lng[nodes1[i]])
    dist[nodes1[i]] = {}
    for j in range(0, len(nodes1)):
        second_elm = (lat[nodes1[j]], lng[nodes1[j]])
        distance1 = geodesic(first_elm, second_elm).km
        dist[nodes1[i]][nodes1[j]] = distance1
        dist[nodes1[j]][nodes1[i]] = distance1

# ******************Graph for edges*********************

graph1 = {}
for i in range(0, len(nodes1)):
    graph1[nodes1[i]] = []

for i in range(0, len(edges)):
    graph1[edges[i][0]].append(edges[i][1])
    graph1[edges[i][1]].append(edges[i][0])


# ***************************Implementing A* to get path between my source and destination************************************

def sort123(openlist12, f_val):
    for i in range(0, len(openlist12)):
        min1 = i
        for j in range(i + 1, len(openlist12)):
            if (f_val[openlist12[j]] < f_val[openlist12[min1]]):
                min1 = j
        if (min1 != i):
            temp = openlist12[min1]
            openlist12[min1] = openlist12[i]
            openlist12[i] = temp
    return openlist12

#******************** To get the Transit Time *************************************

def timefunc(start_pos, end_pos):
    start_pos_lat = lat[start_pos]
    start_pos_lon = lng[start_pos]

    end_lat = lat[end_pos]
    end_lon = lng[end_pos]

    key = 'Aq0cW519uOhs74Y9ncOrtlqz-QlB_3rVeL6O9a8PI-fhgyDCWipKROfV5ROtXoXI'  # Bing maps API key
    print("Sending request to bing maps API")
    url = 'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins='
    url = url + str(start_pos_lat) + ',' + str(start_pos_lon) + '&destinations=' + str(end_lat) + ',' + str(
        end_lon) + '&travelMode=driving&timeUnit=minutes' + '&key=' + key
    data = requests.get(url).text
    json_data = json.loads(data)
    obj = json_data['resourceSets'][0]['resources'][0]['results'][0]
    print("The Time Required for the travel is ",obj['travelDuration'],'minutes')
    print("The Distance Covered is ",obj['travelDistance'],'km')
    return int(re.search(r'\d+', str(obj['travelDuration'])).group())





position = {}
parent = {}
g_val = {}
h_val = {}
f_val = {}
new_parent = {}
new_g_val = {}
new_f_val = {}
for i in nodes1:
    position[i] = i
    g_val[i] = 0
    h_val[i] = 0
    f_val[i] = 0


def aStar(graph1, dist, start, end):
    count = 1
    parent[start] = None
    parent[end] = None

    open_list = []
    closed_list = []

    open_list.append(start)

    while (len(open_list) > 0):

        # print()
        # print('OPEN LIST')
        # print('----------')

        open_list = sort123(open_list, f_val)

        # print('The current node is: '+ position[open_list[0]])
        # print()
        # for item in open_list:
        #     print(position[item] + ' | '+ str(f_val[item]))

        # print('----------')
        # print()
        current_node = open_list.pop(0)
        closed_list.append(current_node)

        # If RGIA is found

        if position[current_node] == position[end]:
            path = []
            current = current_node
            while current is not None:
                path.append(position[current])
                current = parent[current]
            return path[::-1]

        children = []
        temp = graph1[position[current_node]]
        for item in temp:
            new_parent[item] = current_node
            children.append(item)

        # print('CHILDREN OF CURRENT')
        # print('xxxxxxxxxxxxxxxxxxxxxxxxx')

        for child in children:
            if child in closed_list:
                continue
            source = position[current_node]
            dest = position[child]

            new_g_val[child] = g_val[current_node] + dist[source][dest]
            h_val[child] = dist[dest][end]
            new_f_val[child] = new_g_val[child] + h_val[child]

            flag = True
            for node in open_list:
                if position[child] == position[node] and new_f_val[child] < f_val[node]:
                    open_list.remove(node)

                elif position[child] == position[node] and new_f_val[child] > f_val[node]:
                    flag = False
                    continue

            if flag:
                g_val[child] = new_g_val[child]
                f_val[child] = new_f_val[child]
                parent[child] = new_parent[child]
                open_list.append(child)

        # print('xxxxxxxxxxxxxxxxxxxxxxxxx')
        # print() 
        # print('CLOSED LIST')   
        # print('***********************')
        # for item in closed_list:
        #     print(position[item])
        # print('***********************')
        # print()
        # print('#########################################')
        count += 1
    return None


start1234 =  'rgia' # Source node
end1234 = 'birla institute of technology hyderabad'  # Destination
start1234.lower()
end1234.lower()
path1234 = aStar(graph1, dist, start1234, end1234)  # Stores path between source and destination

print('PATH')
print('****************************')
for item in path1234:
    print(item)

timefunc(start1234,end1234)

# ********************** Creating a map to display my path using gmplot library****************************************************


def mapNodes(path):
    latitudes = []
    longitudes = []
    # marker_loc=[]
    print(path)
    for items in path:
        items = str(items)
        latitudes.append(lat[items])
        longitudes.append(lng[items])
        # p=(lat[items],lng[items])
        # marker_loc.append(p)
    #print(latitudes)
    #print(longitudes)
    gmap = gmplot.GoogleMapPlotter(17.3850, 78.4867, 13)

    gmap.plot(latitudes, longitudes, 'blue', edge_width=2.5)
    #gmap.scatter(latitudes, longitudes, '#3B0B39', size=40, marker=False)
    # markers12=gmap.marker_layer(marker_loc)
    # gmap.add_layer(markers12)
    gmap.draw('final1.html')


mapNodes(path1234)
print(g_val)