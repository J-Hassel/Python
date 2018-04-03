#!/usr/bin/env python3
from OSM_Map import OSM_Map as Map
import sys

arguments = sys.argv

my_map = Map("map2.osm")

img = my_map.Route(arguments[1], arguments[2])
my_map.Save("test.pgm")
