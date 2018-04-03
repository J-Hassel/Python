#!/usr/bin/env python3
#from OSM_Map import node


##---------------------------------------- NODE CLASS ----------------------------------------##

class Node:
    def __init__(self, node_id):
        self._id = node_id
#        self._lat = node[node_id][0]
#        self._lon = node[node_id][1]

    @property
    def id(self):
        return self._id

#    @property
#    def lat(self):
#        return self._lat

#    @property
#    def lon(self):
#        return self._lon
