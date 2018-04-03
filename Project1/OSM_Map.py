#!/usr/bin/env python3
import networkx as nx
from lxml import etree
from Node import Node
from PIL import Image, ImageDraw, ImageOps


##---------------------------------------- OSM_MAP CLASS ----------------------------------------##
class OSM_Map:

    def __init__(self, osm_filename):
        doc = etree.parse(osm_filename)

        min_x, self.max_x = float(doc.find("bounds").get("minlon")), float(doc.find("bounds").get("maxlon"))
        min_y, self.max_y = float(doc.find("bounds").get("minlat")), float(doc.find("bounds").get("maxlat"))

        self.width, self.height, self.scaling = self.getImgInfo(min_x, self.max_x, min_y, self.max_y)

        # stores all nodes in a dictionary. {'node ID': ('lat', 'lon')}
        self.node = {}
        for element in doc.findall("node"):
            self.node[element.get("id")] = Node(int(element.get("id")), float(element.get("lat")), float(element.get("lon")))


        # storing all highways in a dictionary. {'highway ID': ['list', 'of', 'nodes', 'in', 'highway']}
        self.highway = {}
        for way in doc.findall("way"):
            for tag in way.findall("tag"):
                if "highway" in tag.get("k"):
                    self.highway[way.get("id")] = []
                    for nd in way.findall("nd"):
                        self.highway[way.get("id")].append(nd.get("ref"))



    def Route(self, src, dest):
        # list of tuples to represent undirected edges in the graph
        edges = []
        for hw in self.highway:
            for i in range(len(self.highway[hw]) - 1):
                edges.append((self.node[self.highway[hw][i]].id, self.node[self.highway[hw][i + 1]].id))

        # creating graph
        G = nx.Graph()
        G.add_edges_from(edges)

        if nx.has_path(G, int(src), int(dest)):
            path = nx.shortest_path(G, int(src), int(dest))
            print(path)


            # print(list(nx.bfs_edges(G, 1)))
        else:
            print("No path exists.")


    def Save(self, img_name):
        bg_color, hw_color, route_color = 255, 150, 50

        img = Image.new('L', (self.width, self.height), color=bg_color)  #creating image
        draw = ImageDraw.Draw(img)

        # draws edges for every separate highway
        for hw in self.highway:
            hw_edges = []
            for i in range(len(self.highway[hw]) - 1):
                hw_edges.append((self.node[self.highway[hw][i]].id, self.node[self.highway[hw][i + 1]].id))

            points = self.convertEdgesToPoints(hw_edges)

            ImageDraw.ImageDraw.line(draw, points, fill=hw_color, width=10)


        img = ImageOps.mirror(img)  #flips image to correct orientation
        img.save(img_name)   #saving image


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
            nd1, nd2 = str(edge[0]), str(edge[1])

            nd1 = self.node[nd1].lon, self.node[nd1].lat
            coords.append(nd1)
            nd2 = self.node[nd2].lon, self.node[nd2].lat
            coords.append(nd2)

        for coord in coords:
            x, y = int((self.max_x - coord[0]) * self.scaling), int((self.max_y - coord[1]) * self.scaling)
            points.append((x, y))

        return points
