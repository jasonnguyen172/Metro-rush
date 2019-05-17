#!/usr/bin/env python3
from functions import *
from metro_graph import *


def main():
    file_name = get_file_name()
    lines = read_file(file_name)
    start_pos, end_pos, trains_number = get_data(lines)
    metrolines = get_metrolines(lines)
    print(metrolines)
    graph = Graph(metrolines, start_pos, end_pos)
    ###########
    # print(graph.nodes_dict['Keshav Puram'].station_id)
    print(graph.end_node.connected)
    # print(find_name_of_station(metrolines, ('Magenta Line', '19')))
    ###########
    # print(graph.nodes['Central Secretariat'].neihgbours)

if __name__ == "__main__":
    main()
