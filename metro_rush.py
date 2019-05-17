#!/usr/bin/env python3
from functions import *
from metro_graph import *


def main():
    file_name = get_file_name()
    lines = read_file(file_name)
    start, end, trains_number = get_data(lines)
    metrolines = get_metrolines(lines)
    graph = Graph(metrolines, start, end)
    ###########
    print(graph.start_node.neihgbours)
    graph.filter_connected_points(metrolines)
    ###########
    # print(graph.nodes['Central Secretariat'].neihgbours)


if __name__ == "__main__":
    main()
