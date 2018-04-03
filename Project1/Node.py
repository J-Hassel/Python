#!/usr/bin/env python3


##---------------------------------------- NODE CLASS ----------------------------------------##

class Node:
    def __init__(self, node_id, lat, lon):
        self._id = node_id
        self._lat = lat
        self._lon = lon

    @property
    def id(self):
        return self._id

    @property
    def lat(self):
        return self._lat

    @property
    def lon(self):
        return self._lon
