#!/usr/bin/env python3
import networkx as nx
from PIL import Image, ImageDraw, ImageOps
from lxml import etree


##---------------------------------------- OSM_MAP CLASS ----------------------------------------##
class OSM_Map:

    def __init__(self, osmFileName):
        doc = etree.parse(osmFileName)

        min_x, self.max_x = float(doc.find("bounds").get("minlon")), float(doc.find("bounds").get("maxlon"))
        min_y, self.max_y = float(doc.find("bounds").get("minlat")), float(doc.find("bounds").get("maxlat"))

        self.width, self.height, self.scaling = self.getImgInfo(min_x, self.max_x, min_y, self.max_y)

        # stores all nodes in a dictionary. {'node ID': ('lat', 'lon')}
        self.node = {}
        for element in doc.findall("node"):
            self.node[element.get("id")] = (element.get("lat"), element.get("lon"))

            # stores the indexes of the nodes in a dictionary. {'node ID': 'index'}
            self.index = {}
            for i, nd in enumerate(self.node):
                self.index[nd] = i

            # stores the node ID for each index in a dictionary. {'Index': 'node ID'}
            self.indexToID = {}
            for i, nd in enumerate(self.node):
                self.indexToID[i] = nd

        # storing all highways in a dictionary. {'highway ID': ['list', 'of', 'nodes', 'in', 'highway']}
        self.highway = {}
        for way in doc.findall("way"):
            for tag in way.findall("tag"):
                if "highway" in tag.get("k"):
                    self.highway[way.get("id")] = []
                    for nd in way.findall("nd"):
                        self.highway[way.get("id")].append(nd.get("ref"))
                        # nd.get("ref"), node[nd.get("ref")])

        # list of tuples to represent undirected edges in the graph
        self.edges = []
        for hw in self.highway:
            for i in range(len(self.highway[hw]) - 1):
                self.edges.append((self.index[self.highway[hw][i]], self.index[self.highway[hw][i + 1]]))

        # creating graph
        self.G = nx.Graph()
        self.G.add_edges_from(self.edges)


    def Route(self, src, dest):
        nd1, nd2 = self.index[src], self.index[dest]

        if nx.has_path(self.G, nd1, nd2):
            path =  nx.shortest_path(self.G, nd1, nd2)
            print(path)


            # print(list(nx.bfs_edges(G, 1)))
        else:
            print("No path exists.")


    def Save(self, imgName):
        bg_color, hw_color, route_color = 255, 150, 50

        img = Image.new('L', (self.width, self.height), color=bg_color)  #creating image
        draw = ImageDraw.Draw(img)


        for hw in self.highway:
            hwEdges = []
            for i in range(len(self.highway[hw]) - 1):
                hwEdges.append((self.index[self.highway[hw][i]], self.index[self.highway[hw][i + 1]]))

            points = self.convertEdgesToPoints(hwEdges)

            #draws edges for every separate highway
            ImageDraw.ImageDraw.line(draw, points, fill=hw_color, width=10)


        img = ImageOps.mirror(img)  #flips image to correct orientation
        img.save(imgName)   #saving image


    def getImgInfo(self, min_x, max_x, min_y, max_y):
        width = max_x - min_x
        height = max_y - min_y
        scaling = 1

        while True:
            width *= 1.1
            height *= 1.1
            scaling *= 1.1

            if width * 1.1 > 4990 or height * 1.1 > 4990:
                break

        return int(round(width) + 10), int(round(height) + 10), scaling


    def convertEdgesToPoints(self, data):
        coords = []
        points = []
        for edge in data:
            nd1, nd2 = edge[0], edge[1]

            nd1 = float(self.node[self.indexToID[nd1]][0]), float(self.node[self.indexToID[nd1]][1])
            coords.append(nd1)
            nd2 = float(self.node[self.indexToID[nd2]][0]), float(self.node[self.indexToID[nd2]][1])
            coords.append(nd2)

        for coord in coords:
            x, y = int((self.max_x - coord[1]) * self.scaling), int((self.max_y - coord[0]) * self.scaling)
            points.append((x, y))

        return points

