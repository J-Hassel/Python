#!/usr/bin/env python3
from Node import Node
from OSM_Map import OSM_Map as Map
import sys

arguments = sys.argv
src = Node(arguments[1])
dest = Node(arguments[2])

map = Map("map2.osm")

img = map.Route(src.id, dest.id)
map.Save("test.pgm")