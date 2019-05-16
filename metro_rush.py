#!/usr/bin/env python3
from argparse import ArgumentParser
from sys import stderr
from re import match


class Node:

    def __init__(self, station_name, station_id, metrolines, connected=False):
        self.station_name = station_name
        # a dict with key= line and value= ID
        # exp: {line1: id1, line2: id2}
        self.station_id = station_id
        #########################
        self.connected = connected
        #########################
        self.neihgbours = None


class Graph:

    def __init__(self, metrolines, start, end):
        self.nodes = set_nodes(metrolines) # {name:{line:id}}
        self.start_node = self.get_start_end_nodes(start)
        self.end_node = self.get_start_end_nodes(end)

    def get_start_end_nodes(self, node):
        print(node)
        for key in self.nodes:
            for sub_key in self.nodes[key].station_id:
                if sub_key == node[0] and self.nodes[key].station_id[sub_key] == node[1]:
                    return self.nodes[key]
    ########################
    def filter_connected_points(self, metrolines):
        for key in self.nodes:
            if self.nodes[key].connected:
                self.find_neihgbours(self.nodes[key], metrolines)

    def find_neihgbours(self, node, metrolines):
        neihgbours = []
        for line in node.station_id:
            tempo = []
            for station in metrolines[line]:
                if ":Conn:" in station and line in node.station_id.keys():
                    tempo.append(station)
            for index, element in enumerate(tempo):
                try:
                    if node.station_name in element and index != 0:
                        neihgbours.append(self.nodes[tempo[index - 1].split(':')[1]])
                        neihgbours.append(self.nodes[tempo[index + 1].split(':')[1]])
                    elif node.station_name in element and index == 0:
                        neihgbours.append(self.nodes[tempo[index + 1].split(':')[1]])
                except:
                    pass
        node.neihgbours = neihgbours
    ########################


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


def main():
    file_name = get_file_name()
    lines = read_file(file_name)
    start, end, trains_number = get_data(lines)
    metrolines = get_metrolines(lines)
    graph = Graph(metrolines, start, end)
    ###########
    graph.filter_connected_points(metrolines)
    ###########
    print(graph.nodes['Central Secretariat'].neihgbours)


if __name__ == "__main__":
    main()
