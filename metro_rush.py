#!/usr/bin/env python3
from argparse import ArgumentParser
from sys import stderr
from re import match




class Graph:

    def __init__(self, metrolines, start, end):
        self.nodes = set_nodes(metrolines, start, end)  # {line:{station:node}}
        self.start_node = self.nodes[start[0]][start[1]]
        self.end_node = self.nodes[end[0]][end[1]]

    def find_way():
        way = None
        return way


def get_station_data(limitation, metroline, station, start, end):
    interchange = [metroline]
    station_id = station.split(":")[0]
    station_name = station.split(":")[1]
    if ":Conn:" in station:
        interchange += station.split(":Conn: ")[1:]
    if (metroline == start[0] and station_id == start[1]) or\
            (metroline == end[0] and station_id == end[1]):
        limitation = False

    return station_id, limitation, interchange, station_name


def set_nodes(metrolines, start, end):
    nodes = {}
    interchange = []
    for metroline in metrolines:
        for station in metrolines[metroline]:
            station_id, limitation, interchange, station_name = get_station_data(True, metroline, station, start, end)
            node = Node(station_id, limitation, interchange, station_name)
            if metroline not in nodes:
                nodes[metroline] = {station_id: node}
            else:
                nodes[metroline].update({station_id: node})
    return nodes


def get_metrolines(lines):
    metrolines = {}
    metroline = None
    for index, line in enumerate(lines):
        if line.startswith("#"):
            metroline = line.replace("#","")
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


def get_connecting_point(metrolines):
    conn_pts_dict = {}
    for line in metrolines:
        for station in metrolines[line]:
            if 'Conn' in station:
                if line not in conn_pts_dict:
                    conn_pts_dict[line] = [station]
                else:
                    conn_pts_dict[line].append(station)
    return conn_pts_dict

class Connect_pts:

    def __init__(self, station_name, station_id, conn_pts):
        self.station_id = station_id
        self.station_name = station_name

def main():
    file_name = get_file_name()
    lines = read_file(file_name)
    start, end, trains_number = get_data(lines)
    metrolines = get_metrolines(lines)
    conn_pts_dict = get_connecting_point(metrolines)

    for line in conn_pts_dict:
        for index, conn_pts in enumerate(conn_pts_dict[line]):
            conn_pts_list = []
            id, station_name, conn, link_line = conn_pts.split(':')
            link_line = link_line[1:]
            print(line)
            print(conn_pts_dict[line])
            print(link_line)
            print(conn_pts_dict[link_line])
            if index == len(conn_pts_dict[line]) - 1:
                conn_pts_list += [conn_pts_dict[line][index-1]]
            elif index == 0:
                conn_pts_list += [conn_pts_dict[line][index+1]]
            else:
                conn_pts_list += [conn_pts_dict[line][index-1],conn_pts_dict[line][index+1]]
            print('dsssssssssssssssssssssssssssssssssssssssssssss')
            print(conn_pts_list)
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
