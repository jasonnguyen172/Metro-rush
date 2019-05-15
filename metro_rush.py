#!/usr/bin/env python3
from argparse import ArgumentParser
from sys import stderr
from re import match


class Graph:

    def __init__(self, metrolines, start, end):
        #start(line, id)
        self.nodes = set_nodes(metrolines)  # {name:{line:id}}
        ################
        self.start_node = self.get_start_end_nodes(start)
        self.end_node = self.get_start_end_nodes(end)
        ################


    def get_start_end_nodes(self, node):
        print(node)
        for key in self.nodes:
            for sub_key in self.nodes[key].station_id:
                if sub_key == node[0] and self.nodes[key].station_id[sub_key] == node[1]:
                    return self.nodes[key]


    def abc(self, metrolines):
        for key in self.nodes:
            if self.nodes[key].conn_pts:
                self.find_neigbours(self.nodes[key], metrolines)


    def find_neigbours(self, node, metrolines):
        neigbour = []
        for line in node.station_id:
            tempo = []
            for station in metrolines[line]:
                if ":Conn:" in station:
                    tempo.append(station)
                    for index, j in enumerate(tempo):
                        try:
                            if node.station_name in j and index != 0:
                                neigbour.append(tempo[index - 1])
                                neigbour.append(tempo[index + 1])
                            elif node.station_name in j and index == 0:
                                neigbour.append(tempo[index + 1])
                        except:
                            pass
        node.neigbours = list(set(neigbour))

    ################
    def find_way():
        way = None
        return way

class Node:

    def __init__(self, station_name, station_id, metrolines, conn_pts=False):
        self.station_name = station_name
        # a dict contains tuples which are station ids of station
        # exp: {(line1: id1), (line2: id2)}
        self.station_id = station_id
        self.conn_pts = conn_pts
        self.neigbours = None


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
                conn_pts = True
            else:
                id, station_name = station.split(':')
                conn_pts = False
            if station_name not in node_dict:
                node_dict[station_name] = Node(station_name,
                                               {line: id}, metrolines, conn_pts)
            else:
                node_dict[station_name].station_id[line] = id
    return node_dict


def find_neigbours_conn_pts(src_node, nodes_list):
    print(src_node.station_id.keys())
    neigbours_list = []
    for node in nodes_list:
        if node.conn_pts is True and get_edge(src_node, node) is not None:
            neigbours_list += [node]
    return neigbours_list


def get_edge(src_conn_node, dest_conn_node):
    for line in src_conn_node.station_id:
        if line in dest_conn_node.station_id:
            return abs(int(src_conn_node.station_id[line]) - int(dest_conn_node.station_id[line]))

def main():
    file_name = get_file_name()
    lines = read_file(file_name)
    start, end, trains_number = get_data(lines)
    metrolines = get_metrolines(lines)
    ################
    graph = Graph(metrolines, start, end)
    #################
    # print(graph.start_node)
    # print(graph.end_node)
    station1 = graph.nodes['Kashmere Gate']
    station2 = graph.nodes['Mandi House']
    # print(get_edge(station1, station2))
    # print(metrolines)
    graph.abc(metrolines)
    print(graph.nodes['Kashmere Gate'].neigbours)

    #print([node.station_name for node in find_neigbours_conn_pts(station1, graph.nodes.values())])
    # print(graph.get_edge())
    #print(graph.get_start_end_nodes(start, end))

    # print((node_dict))
    # print(node_dict['Pragati Maidan'].conn_pts)


    # for line in conn_pts_dict:
    #     for index, conn_pts in enumerate(conn_pts_dict[line]):
    #         conn_pts_list = []
    #         id, station_name, conn, link_line = conn_pts.split(':')
    #         link_line = link_line[1:]
    #         print(line)
    #         print(conn_pts_dict[line])
    #         print(link_line)
    #         print(conn_pts_dict[link_line])
    #         if index == len(conn_pts_dict[line]) - 1:
    #             conn_pts_list += [conn_pts_dict[line][index-1]]
    #         elif index == 0:
    #             conn_pts_list += [conn_pts_dict[line][index+1]]
    #         else:
    #             conn_pts_list += [conn_pts_dict[line][index-1],conn_pts_dict[line][index+1]]
    #         print('dsssssssssssssssssssssssssssssssssssssssssssss')
    #         print(conn_pts_list)
            # for station in conn_pts_dict[link_line]:
                # print(station)
            # if station_name n?ot in dict:
                # dict[station_name] =

    #     print(conn_pts.split(': ')[-1])
        # print(conn_pts[line+2:])
    # print(metrolines)

    # print(*{line: metrolines[line] for line in metrolines}.items(), sep='\n\n')
    # graph = Graph(metrolines, start, end)
    # print(graph.nodes)


if __name__ == "__main__":
    main()
