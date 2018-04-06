#!/usr/bin/env python3
from OSM_Map import OSM_Map as Map
import sys

#command line arguments
arguments = sys.argv
node_id1 = arguments[1]
node_id2 = arguments[2]
input_filename = arguments[3]
output_filename = arguments[4]

my_map = Map(input_filename)

my_map.Route(node_id1, node_id2)
my_map.Save(output_filename)
