from argparse import ArgumentParser
from sys import stderr
from re import match
from station_nodes import Node


def get_metrolines(lines):
    metrolines = {}
    metroline = None
    for index, line in enumerate(lines):
        if line.startswith("#"):
            metroline = line.replace("#", "")
            metrolines[metroline] = []
        elif not line.startswith("START=") and\
                not line.startswith("END=") and\
                not line.startswith("TRAINS") and line:
            metrolines[metroline].append(line)
    return metrolines


def find_words(word_1, word_2, string):
    """
    Find word_1 and word_2 inside a string
    """
    result_1 = match(word_1, string).group(1)
    result_2 = string.replace(word_2 + result_1 + ":", "")

    return (result_1, result_2)


def get_data(lines):
    """
    Get start station, end station and train number
    Return start: tuple(station ID, metro line)
    Return end: tuple(station ID, metro line)
    Return trains_number: train number
    """
    try:
        for line in lines[::-1]:
            if match("START=(.*?):", line):
                start = find_words("START=(.*?):", "START=", line)
            elif match("END=(.*?):", line):
                end = find_words("END=(.*?):", "END=", line)
            elif line.startswith("TRAINS="):
                trains_number = line.replace("TRAINS=", "")
        return start, end, trains_number
    except Exception as e:
        print("Invalid File", file=stderr)
        exit()


def read_file(file_name):
    try:
        open_file = open(file_name, "r")
        lines = open_file.read().splitlines()
        open_file.close()
        return lines
    except Exception:
        print("Error")
        exit()


def get_file_name():
    """
    Get the file name from user's input
    """
    parser = ArgumentParser()
    parser.add_argument('file_name', metavar='file_name')
    args = parser.parse_args()
    return args.file_name


def set_node_info(node_dict, line, id, node_name, connected):
    '''
    Setting attributes for one node of station
    @param node_dict: a dictionary contains all of node which formed:
                      {station_name: station_node_object}
    @param line: line name of station
    @param id: id - index of station
    @param node_name: name of station
    @param connected: boolen value, True if the station is connecting point
    @return: None
    '''
    if node_name not in node_dict:
        node_dict[node_name] = Node(node_name, {line: id}, connected)
    else:
        node_dict[node_name].station_id[line] = id


def get_node_info(info_line):
    '''
    Get information of node from the info_line
    @param info_line: a text line contains info of station
    @return: id - index of station
             node_name - name of station
             connected - boolen value, True if the station is connecting point
    '''
    conn, link_line, connected = None, None, True
    if 'Conn' in info_line:
        id, node_name, conn, link_line = info_line.split(':')
        link_line = link_line[1:]
    else:
        id, node_name = info_line.split(':')
        connected = False
    return int(id), node_name, link_line, connected


def set_nodes(metrolines):
    '''
    Setting attributes for all nodes of station
    @param metrolines: a dictionary contains all of info of stations and lines
                       which formed:
                       {text of line name: text of station info}
    @return: node_dict - a dictionary contains all of node which formed:
                         {text of station name: station_node_object}
    '''
    node_dict = {}
    for line in metrolines:
        for info_line in metrolines[line]:
            id, node_name, link_line, connected = get_node_info(info_line)
            set_node_info(node_dict, line, id, node_name, connected)
    return node_dict


def find_name_of_station(metrolines, position):
    '''
    finding name of a station base on position information
    @param metrolines: a dictionary contains all of info of stations and lines
                       which formed:
                       {text of line name: text of station info}
    @param position: a tuple contains all of info of a station which formed:
                       (text of line name, text of station id)
    '''
    line, id = position
    for info_line in metrolines[line]:
        if id == info_line.split(':')[0]:
            return info_line.split(':')[1]


def get_common_line(source_node, dest_node):
    '''
    find the common line between two node if it available
    @param source_node: type - an object : the first node
    @param dest_node: type - an object : the second node
    @return: - line name if available
             - None if no any common line between 2 node
    '''
    for line in source_node.station_id:
        if line in dest_node.station_id:
            return line


def get_edge(source_node, dest_node):
    '''
    calculate cost of edge between 2 node on one line
    @param source_node: type - an object : the first node
    @param dest_node: type - an object : the second node
    @return: type - int number - length between 2 nodes
             None if 2 nodes are not on one line
    '''
    common_line = get_common_line(source_node, dest_node)
    if common_line:
        return abs(int(source_node.station_id[common_line]) -
                   int(dest_node.station_id[common_line]))
