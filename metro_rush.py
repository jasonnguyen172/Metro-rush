#!/usr/bin/env python3
from functions import get_file_name, read_file, get_data, get_metrolines
from metro_graph import Graph
from station_nodes import Trains
from collections import OrderedDict
from re import match
from implement_dijkstra import find_all_paths, calculate_cost


def move_train(graph, all_paths, distributions, trains_number):
    def modify_path(full_path):
        modified_path = list()
        for station in full_path:
            temporary = list()
            formated_station = station.split('(')[0]
            for train in graph.nodes_dict[formated_station].trains:
                if train != "BLOCKED":
                    temporary.append(train.train_name)
            if graph.nodes_dict[formated_station].trains and "BLOCKED" not in graph.nodes_dict[formated_station].trains:
                modified_path.append(station + '-' + ','.join(temporary))
        return modified_path

    def move(full_path):
        for index, path in enumerate(full_path):
            try:
                if index -1 < 0 and index - 2 < 0:
                    continue
                next_line = match(r"^.*?(\(.*?:)", full_path[index]).group(1)[1:-1]
                current_trains = graph.nodes_dict[full_path[index].split('(')[0]].trains
                previous_trains = graph.nodes_dict[full_path[index - 1].split('(')[0]].trains
                if ("BLOCKED" in current_trains and len(current_trains) == 1) or ("BLOCKED" in previous_trains and len(previous_trains) == 1):
                    continue
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

    def over_limit(each_path, distribution):
        count = []
        for station in each_path[1:-1]:
            station_name = match(r"(.*?\()", station).group(1)
            station_trains = graph.nodes_dict[station_name[0:-1]].trains
            if station_trains:
                count += station_trains
        if len(list(set(count))) >= distribution:
            return True
        return False

    def get_merged_path():
        merged_path = list()
        for each_path in list_paths:
            for station in each_path:
                if station not in merged_path:
                    merged_path.append(station)
        return merged_path

    list_paths = [get_full_path(graph, i) for i in all_paths]
    merged_path = get_merged_path()
    while len(graph.end_node.trains) < trains_number:
        modified_path = []
        for index, each_path in enumerate(list_paths):
            second_station = match(r"(.*?\()", each_path[1]).group(1)
            second_station_trains = graph.nodes_dict[second_station[0:-1]].trains
            if over_limit(each_path, distributions[index]) and "BLOCKED" not in second_station_trains:
                second_station_trains.append("BLOCKED")
            move(each_path[::-1])
        modified_path += modify_path(merged_path)
        print('|'.join(modified_path))


def get_full_path(graph, short_path):
    """
    From a 'raw path' which is in form a list of connected point only
    --> Find a fully path

    @param short_path: raw path

    return full path, which a list of all station that trains will run through
    """
    def get_temporary_path(node, station, temporary_path):
        """
        Find station in graph that matchs the @param station
        Add it to the temporary list
        """
        for key in graph.nodes_dict[node].station_id:
            if key == line and graph.nodes_dict[node].station_id[key] == station:
                temporary_path.append(node + '(' + line + ':'+ str(station) + ')')

    def add_station(full_path, line, stations):
        """
        Generate full path
        """
        temporary_path = list()
        for station in stations:
            for node in graph.nodes_dict:
                get_temporary_path(node, station, temporary_path)
        full_path += temporary_path

    def find_movement_stream(list_connected_station, index, full_path):
        """
        Base on the direction of the train's movement (upstream or downstream)
        reverse list order if train moves downstream (from high ID --> low ID)
        """
        stations = list()
        for line in list_connected_station[index]:
            current_station = list_connected_station[index]
            next_station = list_connected_station[index + 1]
            # upstream, from low ID --> high ID
            if line in next_station and next_station[line] - current_station[line] > 0:
                # keep the order
                stations += [number for number in range(current_station[line], next_station[line] + 1)]
                return line, stations
            # downstream
            elif line in next_station:
                # reverse the order
                stations += [number for number in range(next_station[line], current_station[line] + 1)][::-1]
                return line, stations

    full_path = list()
    # turn list of objects into list of object's attribute ID
    list_connected_station = [node.station_id for node in short_path]
    for index, node in enumerate(list_connected_station):
        try:
            # add stations to the list of full path
            line, stations = find_movement_stream(list_connected_station, index, full_path)
            add_station(full_path, line, stations)
        except IndexError:
            pass
    # remove duplicate stations
    return list(OrderedDict.fromkeys(full_path))


def create_trains(trains_number, graph, start_line):
    """
    Create as many objects for class Trains as number of trains
    """
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
        algorithm = input("Please select an algorithm ('1' or '2'): ")
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

    Return lowest_cost: a tuple: the fastest line, it's cost
    and the delta (different cost between two run)
    """
    for line in distributions:
        current_cost = distributions[line][0]
        delta = distributions[line][1]
        current_cost += delta
        # if found a lower cost, change the current with the new one
        if not lowest_cost[1] or current_cost < lowest_cost[1]:
            lowest_cost = (line, current_cost, delta)
    return lowest_cost


def distribute_train(lines, cost_list, trains_number):
    """
    Distribute a number of trains for each line based on calculation
    In order to get the lowest cost.

    Return a list, with each element is an int
    represent the train number distributed for each line (after sorting)
    """
    distributions = {}
    for index, line in enumerate(lines):
        delta = 1  # for a path that is on one line only
        # for a path that is created from multiple lines
        if not is_connected(line):
            delta = 2
        # store data
        distributions[index] = (cost_list[index], delta, 0)
    for number in range(0, trains_number):
        lowest_cost = (None, None)
        lowest_cost = find_lowest_cost(lowest_cost, distributions)
        train = distributions[lowest_cost[0]][2] + 1
        # change old data with new ones
        distributions[lowest_cost[0]] = (lowest_cost[1], lowest_cost[2], train)
    for key in distributions:
        # reformat data into {key:train_number}
        distributions[key] = distributions[key][2]
    return [distributions[i] for i in sorted(distributions.keys())]


def main():
    # get file name from the user's input
    file_name = get_file_name()
    # read file into a list of lines
    lines = read_file(file_name)
    # get start, end position and trains_number from file
    start_position, end_position, trains_number = get_data(lines)
    # let user select algorithm
    algorithm = select_algorithm()
    # get raw data from file, store it
    metrolines = get_metrolines(lines)
    # create objects of class Graph from raw data
    graph = Graph(metrolines, start_position, end_position)
    # get all connected points
    graph.filter_connected_points(metrolines)
    # create objects of class Trains
    create_trains(int(trains_number), graph, start_position[0])
    # use Dijkstra to fill all possible path (that doesn't pass by each other)
    all_path = find_all_paths(graph.start_node, graph.end_node, graph.nodes_dict)
    #Run algorithm depending on user's choice
    if algorithm == "1":
        # distribute all train to the shortest path
        distributions = [int(trains_number), 0]
        move_train(graph, [all_path[0]], distributions, int(trains_number))
    elif algorithm == "2":
        # calcul total cost of each path
        cost_list = [calculate_cost(line) for line in all_path]
        # calcul number of trains for each path before moving them
        distributions = distribute_train(all_path, cost_list, int(trains_number))
        move_train(graph, all_path, distributions, int(trains_number))


if __name__ == "__main__":
    main()
