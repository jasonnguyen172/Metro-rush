from station_nodes import *
from functions import *

class Graph:

    def __init__(self, metrolines, start, end):
        self.nodes_dict = set_nodes(metrolines) # {name:{line:id}}
        self.start_node = self.get_start_end_nodes(start)
        self.end_node = self.get_start_end_nodes(end)

    def get_start_end_nodes(self, node):
        for key in self.nodes_dict:
            for sub_key in self.nodes_dict[key].station_id:
                if sub_key == node[0] and self.nodes_dict[key].station_id[sub_key] == node[1]:
                    return self.nodes_dict[key]
    ########################
    def filter_connected_points(self, metrolines):
        for key in self.nodes_dict:
            if self.nodes_dict[key].connected:
                self.find_neihgbours(self.nodes_dict[key], metrolines)

    def find_neihgbours(self, node, metrolines):
        neihgbours = []
        for line in node.station_id:
            tempo = []
            for station in metrolines[line]:
                if ":Conn:" in station and line in node.station_id.keys():
                    tempo.append(station)
            for index, element in enumerate(tempo):
                try:
                    if node.station_name in element and index != 0:
                        neihgbours.append(self.nodes_dict[tempo[index - 1].split(':')[1]])
                        neihgbours.append(self.nodes_dict[tempo[index + 1].split(':')[1]])
                    elif node.station_name in element and index == 0:
                        neihgbours.append(self.nodes_dict[tempo[index + 1].split(':')[1]])
                except:
                    pass
        node.neihgbours = neihgbours
