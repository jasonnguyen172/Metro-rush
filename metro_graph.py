from station_nodes import *
from functions import *


class Graph:

    def __init__(self, metrolines, start, end):
        self.nodes_dict = set_nodes(metrolines)  # {name:node_obj}
        self.start_node = self.get_start_end_nodes(metrolines, start)
        self.end_node = self.get_start_end_nodes(metrolines, end)

    def get_start_end_nodes(self, metrolines, position):
        '''
        finding start and end point base on position of them
        @param metrolines: a dictionary contains all of info of stations and
                           lines which formed:
                           {text of line name: text of station info}
        @param position: a tuple contains all of info of a station which
                         formed: (text of line name, text of station id)
        @return: object of start or end node
        '''
        station_name = find_name_of_station(metrolines, position)
        self.nodes_dict[station_name].connected = True
        return self.nodes_dict[station_name]

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
