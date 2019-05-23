#!/usr/bin/env python3
from functions import get_file_name, read_file, get_data, get_metrolines
from metro_graph import Graph
from station_nodes import Train
from collections import OrderedDict
from re import match
from GUI import display
from implement_dijkstra import find_all_paths, calculate_cost


def move_train(graph, all_paths, distributions, trains_number):
    """
    Move trains

    @param: all_paths: all possible paths (that doesn't interchange each other)
    @param: distributions: train number distributed for each path
    """
    def modify_path(full_path):
        """
        From full path, keep all station that has train, remove the rest
        Change to form: <station_name>(<line_name>:<station_id>)-<train_label>

        Return modified_path: a list of stations which is ready to be printed
        """
        modified_path, gui_data = list(), list()
        for station in full_path:
            temporary = list()
            formated_station = station.split('(')[0]
            for train in graph.nodes_dict[formated_station].trains:
                # dont need to keep the station that is BLOCKED
                if train != "BLOCKED":
                    temporary.append(train.train_name)
            # change form
            if graph.nodes_dict[formated_station].trains and\
               "BLOCKED" not in graph.nodes_dict[formated_station].trains:
                modified_path.append(station + '-' + ','.join(temporary))
                gui_data.append(station)
        return (modified_path, gui_data)

    def move(full_path):
        """
        Loop through path, check for trains which are moveable
        Move them by remove their instance from current station
        and add to next station
        """
        for index, path in enumerate(full_path):
            try:
                if index - 1 < 0 and index - 2 < 0:
                    continue
                pattern = r"^.*?(\(.*?:)"
                next_line = match(pattern, full_path[index]).group(1)[1:-1]
                current = graph.nodes_dict[full_path[index].split('(')[0]]
                previous = graph.nodes_dict[full_path[index - 1].split('(')[0]]
                current_trains = current.trains
                previous_trains = previous.trains
                # dont make any move on a station that is blocked
                if "BLOCKED" in current_trains and len(current_trains) == 1:
                    continue
                if "BLOCKED" in previous_trains and len(previous_trains) == 1:
                    continue
                # IF current train's already stopped for one turn
                # OR there is no line change
                # AND current station has train
                # AND next station doesn't have train
                if ((next_line == current_trains[0].current_line
                    or current_trains[0].stay) and current_trains and
                    (not previous_trains or
                     graph.nodes_dict[full_path[index - 1].split('(')[0]]
                     is graph.end_node)):
                    # remove from current station
                    moved_train = current_trains.pop(0)
                    # move to next station
                    previous_trains.append(moved_train)
                    # remove freezing
                    moved_train.stay = False
                    # store the data of current line
                    moved_train.current_line = next_line
                # There is a line change
                elif (next_line != current_trains[0].current_line and
                      current_trains and
                      (not previous_trains or
                       graph.nodes_dict[full_path[index - 1].split('(')[0]]
                       is graph.end_node)):
                    moved_train = current_trains[0]
                    # freeze the train
                    moved_train.stay = True
                    moved_train.current_line = next_line
            except IndexError:
                pass

    def over_limit(each_path, distribution):
        """
        Check if train number in @param:each_path has reached the limit
        Return False by default

        @param: each_path: a possible path

        Return False by default
        """
        count = []
        for station in each_path[1:-1]:
            station_name = match(r"(.*?\()", station).group(1)
            station_trains = graph.nodes_dict[station_name[0:-1]].trains
            # each train on path, count + 1
            if station_trains:
                count += station_trains
        # if train number on path > train number distributed, return True
        if len(list(set(count))) >= distribution:
            return True
        return False

    def get_merged_path():
        """
        Merge all possible paths to one only path

        Return merged_path: list of stations
        """
        merged_path = list()
        for each_path in list_paths:
            for station in each_path:
                if station not in merged_path:
                    merged_path.append(station)
        return merged_path

    # create a list of full path from a list of raw paths
    list_paths = find_all_paths(graph)[1]
    # merge all possible paths to one only path
    merged_path = get_merged_path()
    data_gui = list()
    while len(graph.end_node.trains) < trains_number:
        modified_path = []
        for index, each_path in enumerate(list_paths):
            second_station = match(r"(.*?\()", each_path[1]).group(1)
            this_station = graph.nodes_dict[second_station[0:-1]]
            second_station_trains = this_station.trains
            # block the path by blocking the second station of that path
            if over_limit(each_path, distributions[index]) \
               and "BLOCKED" not in second_station_trains:
                second_station_trains.append("BLOCKED")
            move(each_path[::-1])
        # print result
        modified_path += modify_path(merged_path)[0]
        print('|'.join(modified_path))
        # return data for displaying gui purpose
        data_gui.append(modify_path(merged_path)[1])
    return data_gui


def create_trains(trains_number, graph, start_line):
    """
    Create as many objects for class Trains as number of trains
    """
    for number in range(1, trains_number + 1):
        train_name = 'T' + str(number)
        train = Train(start_line, graph.start_node, train_name)


def select_algorithm():
    """
    Let user select one of the implemented algorithms
    """
    print("Please select one of these algorithms:")
    print("    1. One path for all trains (default)")
    print("    2. Multiple paths with improved heuristic (10-30% better)")
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

    """ Reading data and store data """
    # get file name from the user's input
    file_name, gui = get_file_name()
    # read file into a list of lines
    lines = read_file(file_name)
    # get start, end position and trains_number from file
    start_position, end_position, trains_number = get_data(lines)
    # let user select algorithm
    algorithm = select_algorithm()
    # get raw data from file, store it
    metrolines = get_metrolines(lines)
    # create objects of class Graph from raw data

    """ Creating objects """
    graph = Graph(metrolines, start_position, end_position)
    # get all connected points
    graph.find_neihgbours()
    # create objects of class Trains
    create_trains(int(trains_number), graph, start_position[0])

    """ Find path and move trains """
    # use Dijkstra to fill all possible path (that doesn't pass by each other)
    all_path = find_all_paths(graph)[0]
    # run algorithm depending on user's choice
    if algorithm == "1":
        # distribute all train to the shortest path
        distributions = [int(trains_number), 0]
        data_gui = move_train(graph, [all_path[0]],
                              distributions, int(trains_number))
    elif algorithm == "2":
        # calcul total cost of each path
        cost_list = [calculate_cost(line, graph) for line in all_path]
        # calcul number of trains for each path before moving them
        distributions = distribute_train(all_path, cost_list,
                                         int(trains_number))
        data_gui = move_train(graph, all_path,
                              distributions, int(trains_number))

    """  Display GUI """
    if gui and data_gui:
        display(graph, data_gui)
    elif gui:
        print("NO PATH FOUND: cannot run GUI")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
