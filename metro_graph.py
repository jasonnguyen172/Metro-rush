from station_nodes import Node
from functions import (set_nodes, find_name_of_station, set_lines_dict,
                       get_interchange_dict, check_circular_line)


class Graph:
    """
    Store all informations of the metro
    Including all station's instance
    """
    def __init__(self, metrolines, start, end):
        self.nodes_dict = set_nodes(metrolines)  # {name:node_obj}
        # store start, end nodes
        self.start_node = self.get_start_end_nodes(metrolines, start)
        self.end_node = self.get_start_end_nodes(metrolines, end)
        # {line:[node,node]}
        self.lines_dict = set_lines_dict(self.nodes_dict, metrolines)
        # store all interchange nodes
        self.interchange_dict = get_interchange_dict(self.lines_dict)
        self.circular_lines_list = check_circular_line(metrolines)

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

    def find_neihgbours(self):
        for line_name in self.lines_dict:
            temporary_list = []
            for node in self.lines_dict[line_name]:
                if node.connected:
                    temporary_list.append(node)
            if len(temporary_list) > 2:
                for index, node in enumerate(temporary_list[1:-1], 1):
                    node.neihgbours += [temporary_list[index - 1],
                                        temporary_list[index + 1]]
                if line_name in self.circular_lines_list:
                    temporary_list[0].neihgbours += [temporary_list[-1],
                                                     temporary_list[1]]
                    temporary_list[-1].neihgbours += [temporary_list[-2],
                                                      temporary_list[0]]
                else:
                    temporary_list[0].neihgbours += [temporary_list[1]]
                    temporary_list[-1].neihgbours += [temporary_list[-2]]
            elif len(temporary_list) == 2:
                temporary_list[0].neihgbours += [temporary_list[1]]
                temporary_list[-1].neihgbours += [temporary_list[-2]]
