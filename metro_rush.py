#!/usr/bin/env python3
from functions import *
from metro_graph import *
import json  # using for print test


def main():
    file_name = get_file_name()
    lines = read_file(file_name)
    start_pos, end_pos, trains_number = get_data(lines)
    metrolines = get_metrolines(lines)
    # print(metrolines)
    graph = Graph(metrolines, start_pos, end_pos)
    graph.filter_connected_points(metrolines)
    ###########
    # print('aaa')
    print([nei.station_name for nei in graph.nodes_dict['Netaji Subhash Place'].neihgbours])
    print(get_edge(graph.end_node, graph.nodes_dict['Botanical Garden']))
    # print([nei.station_name for nei in graph.start_node.neihgbours])
    # print(graph.end_node.neihgbours)
    # print(find_name_of_station(metrolines, ('Magenta Line', '19')))
    ###########
    # print(graph.nodes['Central Secretariat'].neihgbours)
    # print(json.dumps(get_conn_pts_dict(metrolines), indent=4))

    # find_neihgbours(metrolines)

if __name__ == "__main__":
    main()
