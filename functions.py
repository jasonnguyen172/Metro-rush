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
        if connected:
            node_dict[node_name].station_id[line] = id
        else:
            pass


def get_node_info(info_line):
    '''
    Get information of node from the info_line
    @param info_line: a text line contains info of station
    @return: id - index of station
             node_name - name of station
             connected - boolen value, True if the station is connecting point
    '''
    link_line, connected = None, True
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


def set_lines_dict(nodes_dict, metrolines):
    '''
    create a dictionary which formed: {line name: node_obj}
    @param nodes_dict: dictionary contains node_name as key and value is
                       node object
    @param metrolines: a dictionary contains all of info of stations and lines
                       which formed:
                       {text of line name: text of station info}
    @return lines_dict:  dictionary which formed: {line name: node_obj}
    '''
    lines_dict = {}
    for line_name in metrolines:
        lines_dict[line_name] = []
        for text_line in metrolines[line_name]:
            station_name = text_line.split(':')[1]
            lines_dict[line_name].append(nodes_dict[station_name])
    return lines_dict


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


def check_circular_line(metrolines):
    '''
    check and find out all of circular lines in graph
    @param metrolines: a dictionary contains all of info of stations and lines
                       which formed:
                       {text of line name: text of station info}
    @return circular_lines_list: list of all name of circular lines
    '''
    circular_lines_list = []
    for line_name in metrolines:
        if metrolines[line_name][0].split(':')[1] ==\
           metrolines[line_name][-1].split(':')[1]:
            circular_lines_list.append(line_name)
    return circular_lines_list


def get_interchange_dict(lines_dict):
    '''
    get a dictionary which show all of interchanges on a line
    @param lines_dict: dictionary which formed: {line name: node_obj}
    @return interchange_dict: dictionary which formed:
                              {line name: interchange nodes}
    '''
    interchange_dict = {}
    for line_name in lines_dict:
        interchange_dict[line_name] = []
        for node in lines_dict[line_name]:
            if node.connected:
                interchange_dict[line_name].append(node)
    return interchange_dict


def get_edge(source_node, dest_node, graph):
    '''
    calculate cost of edge from a node to the nearest node
    @param source_node: type - an object : the first node
    @param dest_node: type - an object : the second node
    @return: type - int number - length between 2 nodes
             None if 2 nodes are not on one line
    '''
    if dest_node not in source_node.neihgbours:
        print('2 nodes were not neighboured')
        return
    common_line = get_common_line(source_node, dest_node)
    source_id = source_node.station_id[common_line]
    dest_id = dest_node.station_id[common_line]
    length_line = len(graph.lines_dict[common_line])
    interchange_list = graph.interchange_dict[common_line]
    # if there is more than 2 interchanges in line
    if len(interchange_list) > 2:
        # if moving from the first interchange node to the last interchange
        # node directly in circular line, or backward
        if abs(interchange_list.index(source_node) -
               interchange_list.index(dest_node)) > 1:
                return abs(length_line - max(source_id, dest_id) +
                           min(source_id, dest_id) - 1)
        else:
            return abs(source_id - dest_id)
    # get the smallest cost if there is just 2 interchanges in line
    else:
        return min(abs(source_id - dest_id),
                   abs(length_line - max(source_id, dest_id) +
                   min(source_id, dest_id) - 1))
