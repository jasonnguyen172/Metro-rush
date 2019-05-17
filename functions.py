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
        elif not line.startswith("START=") and not line.startswith("END=") and not line.startswith("TRAINS") and line:
            metrolines[metroline].append(line)
    return metrolines


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
                metro_line = match("START=(.*?):", line).group(1)
                ID = line.replace("START=" + metro_line + ":", "")
                start = (metro_line, ID)
            elif match("END=(.*?):", line):
                metro_line = match("END=(.*?):", line).group(1)
                ID = line.replace("END=" + metro_line + ":", "")
                end = (metro_line, ID)
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


def set_nodes(metrolines):
    node_dict = {}
    for line in metrolines:
        for station in metrolines[line]:
            if 'Conn' in station:
                id, station_name, conn, link_line = station.split(':')
                link_line = link_line[1:]
                connected = True
            else:
                id, station_name = station.split(':')
                connected = False
            if station_name not in node_dict:
                node_dict[station_name] = Node(station_name,
                                               {line: id}, metrolines, connected)
            else:
                node_dict[station_name].station_id[line] = id
    return node_dict


def find_neihgbours_connected(src_node, nodes_list):
    print(src_node.station_id.keys())
    neihgbours_list = []
    for node in nodes_list:
        if node.connected is True and get_edge(src_node, node) is not None:
            neihgbours_list += [node]
    return neihgbours_list


def get_edge(src_conn_node, dest_conn_node):
    for line in src_conn_node.station_id:
        if line in dest_conn_node.station_id:
            return abs(int(src_conn_node.station_id[line]) - int(dest_conn_node.station_id[line]))
