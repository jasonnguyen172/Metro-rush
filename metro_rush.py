#!/usr/bin/env python3
from functions import *
from metro_graph import *
from collections import OrderedDict
from re import match
from implement_dijkstra import find_all_paths, calculate_cost


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
                if (next_line == current_trains[0].current_line or current_trains[0].stay) and current_trains and (not previous_trains or graph.nodes_dict[full_path[index - 1].split('(')[0]] is graph.end_node):
                    moved_train = current_trains.pop(0)
                    previous_trains.append(moved_train)
                    moved_train.stay = False
                    moved_train.current_line = next_line
                elif (next_line != current_trains[0].current_line) and current_trains and (not previous_trains or graph.nodes_dict[full_path[index - 1].split('(')[0]] is graph.end_node):
                    moved_train = current_trains[0]
                    moved_train.stay = True
                    moved_train.current_line = next_line
            except IndexError:
                pass

    while len(graph.end_node.trains) < trains_number:
        move(full_path[::-1])
        modify_path(full_path)


def get_full_path(graph, short_path):
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
    list_connected_station = [node.station_id for node in short_path]
    for index, node in enumerate(list_connected_station):
        try:
            line, stations = find_movement_stream(list_connected_station, index, full_path)
            add_station(full_path, line, stations)
        except IndexError:
            pass
    return list(OrderedDict.fromkeys(full_path))


def create_trains(trains_number, graph, start_line):
    for number in range (1, trains_number + 1):
        train_name = 'T' + str(number)
        train = Trains(start_line, graph.start_node, train_name)


def select_algorithm():
    """
    Let user select one of the implemented algorithms
    """
    print("Please select one of these algorithms:")
    print("    1. One path for all trains (default)")
    print("    2. Multiple paths with improved heuristic (generally 10-30% better)")
    print("If none is selected, default option will be run automatically.")

    # loop until a valid algorithm is selected
    while True:
        algorithm = input("Please select algorithm ('1' or '2'): ")
        # set '1' to be the default algorithm
        if not algorithm:
            return '1'
        elif str(algorithm) in ['1', '2']:
            return algorithm
        # if user's input is invalid, let user input again
        else:
            print("Input must be '1' or '2', please try again")


def is_connected(line):
    """
    Check if path is created from multiple lines
    Return False by default
    """
    # if a line-change found, return True
    for key in line[0].station_id:
        if key in line[-1].station_id:
            return True
    return False


def find_lowest_cost(lowest_cost, distributions):
    """
    Change current lowest cost if a new one is found
    """
    for line in distributions:
        current_cost = distributions[line][0]
        delta = distributions[line][1]
        current_cost += delta
        if not lowest_cost[1] or current_cost < lowest_cost[1]:
            lowest_cost = (line, current_cost, delta)
    return lowest_cost


def distribute_train(lines, cost_list, trains_number):
    """
    Distribute a number of trains for each line based on calculation
    In order to get the lowest cost.
    """
    distributions = {}
    for index, line in enumerate(lines):
        delta = 1  # for a path that is on one line only
        # for a path that is created from multiple lines
        if not is_connected(line):
            delta = 2
        distributions[index] = (cost_list[index], delta, 0)
    for number in range(0, trains_number):
        lowest_cost = (None, None)
        lowest_cost = find_lowest_cost(lowest_cost, distributions)
        train = distributions[lowest_cost[0]][2] + 1
        distributions[lowest_cost[0]] = (lowest_cost[1], lowest_cost[2], train)
    for key in distributions:
        distributions[key] = distributions[key][2]
    return distributions


def main():
    file_name = get_file_name()
    lines = read_file(file_name)
    start_pos, end_pos, trains_number = get_data(lines)
    algorithm = select_algorithm()
    metrolines = get_metrolines(lines)
    graph = Graph(metrolines, start_pos, end_pos)
    graph.filter_connected_points(metrolines)
    create_trains(int(trains_number), graph, start_pos[0])
    all_path = find_all_paths(graph.start_node, graph.end_node, graph.nodes_dict)
    if algorithm == "1":
        full_path = get_full_path(graph, all_path[0])
        move_train(graph, int(trains_number), full_path)
    elif algorithm == "2":
         cost_list = [calculate_cost(line) for line in all_path]
         distributions = distribute_train(all_path, cost_list, int(trains_number))
         print(distributions)


if __name__ == "__main__":
    main()
