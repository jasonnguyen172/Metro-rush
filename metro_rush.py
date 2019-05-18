#!/usr/bin/env python3
from functions import *
from metro_graph import *
from breadth_first_search import implement_bfs
import json  # using for print test


def get_full_path(graph):
    def get_temporary_path(node, station, temporary_path):
        for key in graph.nodes_dict[node].station_id:
            if key == line and graph.nodes_dict[node].station_id[key] == station:
                temporary_path.append(node)

    def add_station(full_path, line, stations):
        temporary_path = []
        for station in stations:
            for node in graph.nodes_dict:
                get_temporary_path(node, station, temporary_path)
        full_path += temporary_path

    def find_movement_stream(list_connected_station, index, full_path):
        stations = []
        for line in list_connected_station[index]:
            if line in list_connected_station[index + 1] and list_connected_station[index + 1][line] - list_connected_station[index][line] > 0:
                stations += [number for number in range(list_connected_station[index][line], list_connected_station[index + 1][line] + 1)]
                return line, stations
            elif line in list_connected_station[index + 1]:
                stations += [number for number in range(list_connected_station[index + 1][line], list_connected_station[index][line] + 1)][::-1]
                return line, stations

    full_path = []
    list_connected_station = [node.station_id for node in implement_bfs(graph.start_node, graph.end_node)]
    for index, node in enumerate(list_connected_station):
        try:
            line, stations = find_movement_stream(list_connected_station, index, full_path)
            add_station(full_path, line, stations)
        except IndexError:
            pass
    return full_path




def main():
    file_name = get_file_name()
    lines = read_file(file_name)
    start_pos, end_pos, trains_number = get_data(lines)
    metrolines = get_metrolines(lines)
    # print(metrolines)
    graph = Graph(metrolines, start_pos, end_pos)
    graph.filter_connected_points(metrolines)
    print(get_full_path(graph))
    ###########
    # print('aaa')
    #print([nei.station_name for nei in graph.nodes_dict['Netaji Subhash Place'].neihgbours])
    #print(get_edge(graph.end_node, graph.nodes_dict['Botanical Garden']))
    # print([nei.station_name for nei in graph.start_node.neihgbours])
    # print(graph.end_node.neihgbours)
    # print(find_name_of_station(metrolines, ('Magenta Line', '19')))
    ###########
    # print(graph.nodes['Central Secretariat'].neihgbours)
    # print(json.dumps(get_conn_pts_dict(metrolines), indent=4))

    # find_neihgbours(metrolines)

if __name__ == "__main__":
    main()
