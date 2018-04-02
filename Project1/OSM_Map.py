#!/usr/bin/env python3
import networkx as nx
from lxml import etree

doc = etree.parse("map2.osm")

min_x = doc.find("bounds").get("minlon")
max_x = doc.find("bounds").get("maxlon")
min_y = doc.find("bounds").get("minlat")
max_y = doc.find("bounds").get("maxlat")

# stores all nodes in a dictionary. {'node ID': ('lat', 'lon')}
node = {}
for element in doc.findall("node"):
    node[element.get("id")] = (element.get("lat"), element.get("lon"))

# stores the indexes of the nodes in a dictionary. {'node ID': 'index'}
index = {}
for i, nd in enumerate(node):
    index[nd] = i

# storing all highways in a dictionary. {'highway ID': ['list', 'of', 'nodes', 'in', 'highway']}
highway = {}
for way in doc.findall("way"):
    for tag in way.findall("tag"):
        if "highway" in tag.get("k"):
            highway[way.get("id")] = []
            for nd in way.findall("nd"):
                highway[way.get("id")].append(nd.get("ref"))
                # nd.get("ref"), node[nd.get("ref")])

# list of tuples to represent undirected edges in the graph
edges = []
for hw in highway:
    for i in range(len(highway[hw]) - 1):
        edges.append((index[highway[hw][i]], index[highway[hw][i + 1]]))

# creating graph
G = nx.Graph()
G.add_edges_from(edges)


##---------------------------------------- OSM_MAP CLASS ----------------------------------------##
class OSM_Map:

    def plot_route(self, start, finish):
        nd1, nd2 = index[start], index[finish]

        if nx.has_path(G, nd1, nd2):
            return nx.shortest_path(G, nd1, nd2)
            # print(list(nx.bfs_edges(G, 1)))
        else:
            print("No path exists.")

    def save(self):
        pass
