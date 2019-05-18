from argparse import ArgumentParser
from sys import stderr
from re import match
from station_nodes import *


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


# def get_conn_pts_dict(metrolines):
#     '''
#     Create a dictionary of connecting points
#     '''
#     conn_point_dict = {}
#     for line_name in metrolines:
#         conn_point_dict[line_name] = []
#         for text_line in metrolines[line_name]:
#             conn_point_dict[line_name] += [text_line] \
#              if 'Conn' in text_line else []
#     return conn_point_dict
#
#
# def find_neihgbours(metrolines):
#     '''
#     @param metrolines: a dictionary contains all of info of stations and lines
#                        which formed:
#                        {text of line name: text of station info}
#     '''
#     conn_point_dict = get_conn_pts_dict(metrolines)
#     neihgbours_dict = {}
#     for line_name in conn_point_dict:
#         for text_line in conn_point_dict[line_name]:
#             id, node_name, link_line, connected = get_node_info(text_line)
#             print(id, node_name, link_line, connected, sep=':')


# def find_neihgbours_connected(src_node, nodes_list):
#     print(src_node.station_id.keys())
#     neihgbours_list = []
#     for node in nodes_list:
#         if node.connected is True and get_edge(src_node, node) is not None:
#             neihgbours_list += [node]
#     return neihgbours_list


def get_edge(src_conn_node, dest_conn_node):
    for line in src_conn_node.station_id:
        if line in dest_conn_node.station_id:
            return abs(int(src_conn_node.station_id[line]) -
                       int(dest_conn_node.station_id[line]))
