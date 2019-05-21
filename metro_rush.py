#!/usr/bin/env python3
from functions import *
from metro_graph import *
from collections import OrderedDict
from re import match
from implement_dijkstra import find_all_path


def move_train(graph, trains_number, full_path):
    def modify_path(full_path):
        modified_path = list()
        for station in full_path:
            temporary = list()
            formated_station = station.split('(')[0]
            for train in graph.nodes_dict[formated_station].trains:
                temporary.append(train.train_name)
            if graph.nodes_dict[formated_station].trains:
                modified_path.append(station + '-' + ','.join(temporary))
        print('|'.join(modified_path))

    def move(full_path):

        for index, path in enumerate(full_path):
            try:
                if index -1 < 0 and index - 2 < 0:
                    continue
                next_line = match(r"^.*?(\(.*?:)", full_path[index]).group(1)[1:-1]
                current_trains = graph.nodes_dict[full_path[index].split('(')[0]].trains
                previous_trains = graph.nodes_dict[full_path[index - 1].split('(')[0]].trains
                if (next_line == current_line or current_trains[0].stay) and current_trains and (not previous_trains or graph.nodes_dict[full_path[index - 1].split('(')[0]] is graph.end_node):
                    moved_train = current_trains.pop(0)
                    previous_trains.append(moved_train)
                    moved_train.stay += False
                elif (next_line != current_line) and current_trains and (not previous_trains or graph.nodes_dict[full_path[index - 1].split('(')[0]] is graph.end_node):
                    moved_train = current_trains[0]
                    moved_train.stay += True
            except IndexError:
                pass

    current_line = match(r"^.*?(\(.*?:)", full_path[1]).group(1)[1:-1]
    while len(graph.end_node.trains) < trains_number:
        move(full_path[::-1])
        modify_path(full_path)


def get_full_path(graph):
    def get_temporary_path(node, station, temporary_path):
        for key in graph.nodes_dict[node].station_id:
            if key == line and graph.nodes_dict[node].station_id[key] == station:
                temporary_path.append(node + '(' + line + ':'+ str(station) + ')')

    def add_station(full_path, line, stations):
        temporary_path = list()
        for station in stations:
            for node in graph.nodes_dict:
                get_temporary_path(node, station, temporary_path)
        full_path += temporary_path

    def find_movement_stream(list_connected_station, index, full_path):
        stations = list()
        for line in list_connected_station[index]:
            if line in list_connected_station[index + 1] and list_connected_station[index + 1][line] - list_connected_station[index][line] > 0:
                stations += [number for number in range(list_connected_station[index][line], list_connected_station[index + 1][line] + 1)]
                return line, stations
            elif line in list_connected_station[index + 1]:
                stations += [number for number in range(list_connected_station[index + 1][line], list_connected_station[index][line] + 1)][::-1]
                return line, stations

    full_path = list()
    list_connected_station = [node.station_id for node in find_all_path(graph.start_node, graph.end_node, graph.nodes_dict)[0]]
    for index, node in enumerate(list_connected_station):
        try:
            line, stations = find_movement_stream(list_connected_station, index, full_path)
            add_station(full_path, line, stations)
        except IndexError:
            pass
    return list(OrderedDict.fromkeys(full_path))


def create_trains(trains_number, graph):
    for number in range (1, trains_number + 1):
        train_name = 'T' + str(number)
        train = Trains(graph, graph.start_node, train_name)


def select_algorithm():
    """
    Let user select one of the implemented algorithms
    """
    print("Please select one of these algorithms:")
    print("    1. One path for all trains (default)")
    print("    2. Multiple path with improved heuristic")
    print("If none is selected, default option will be run automatically.")

    # loop until a valid algorithm is selected
    while True:
        algorithm = input("Please select algorithm ('1' or '2'): ")
        # nearest neighbor is the default algorithm
        if not algorithm:
            return '1'
        elif str(algorithm) in ['1', '2']:
            return algorithm
        # if user's input is invalid, let user input again
        else:
            print("Input must be '1' or '2', please try again")


def main():
    file_name = get_file_name()
    lines = read_file(file_name)
    start_pos, end_pos, trains_number = get_data(lines)
    algorithm = select_algorithm()
    metrolines = get_metrolines(lines)
    graph = Graph(metrolines, start_pos, end_pos)
    graph.filter_connected_points(metrolines)
    create_trains(int(trains_number), graph)
    full_path = get_full_path(graph)
    if algorithm == "1":
        move_train(graph, int(trains_number), full_path)
    # elif algorithm == "2":
    #     all_path = find_all_path(graph.start_node, graph.end_node, graph.nodes_dict)
    #     for _path in all_path:
    #         print([i.station_name for i in _path])


if __name__ == "__main__":
    main()
