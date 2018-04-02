#!/usr/bin/env python3
from Node import Node
from OSM_Map import OSM_Map as Map
import sys

arguments = sys.argv
start = Node(arguments[1])
finish = Node(arguments[2])

route = Map()

path = route.plot_route(start.id, finish.id)
print(path)
route.save()