from functions import *
from math import inf


def validate_new_nodes(current_node, new_nodes_list, close_list,
                       open_list, previous_node, cost_dict):
    '''
    validate all new nodes if its the next considered nodes
    @parram current_node: the current considered node
    @parram new_nodes_list: a list contains all new nodes extanded from
                            current_node
    @parram close_list: a list contains nodes which be considered
    @parram open_list: a list contains nodes which not be considered yet
    @parram previous_node: a dictionary contains a previous node of a
                           particular node ({node_x : prev_node_x})
    @param cost_dict: a dictionary showing cost from start node to a particular
                      node, formed : {node_x: cost_x}
    @return open_list: a list contains validated nodes which not be
                       considered yet
    '''
    for new_node in new_nodes_list:
        if new_node in close_list:
            continue
        if new_node in open_list:
            new_cost = get_edge(current_node, new_node) +\
                       cost_dict[current_node]
            if new_cost >= cost_dict[new_node]:
                continue
        # set information for validated new node
        previous_node[new_node] = current_node
        cost_dict[new_node] = get_edge(current_node, new_node) +\
            cost_dict[current_node]
        open_list.append(new_node)
    return open_list


def find_new_nodes(current_node, all_nodes_list):
    '''
    extend all neihgbour nodes from a current node for the next considered
    nodes
    @parram current_node: the current considered node
    @param all_nodes_list: a dictionary showing cost from start node to a
                       particular node, formed : {node_x: cost_x}
    @return new_nodes_list: list contains all new nodes
    '''
    new_nodes_list = []
    for node in current_node.neihgbours:
        if node in all_nodes_list:
            new_nodes_list.append(node)
    return new_nodes_list


def track_back(start_node, end_node, previous_node):
    '''
    track back from end_node to the start_node to find the shortest path
    @param start_node: the start station of trains
    @param end_node: the destination of the trains
    @param previous_node: a dictionary contains a previous node of a
                          particular node ({node_x : prev_node_x})
    @return path: a list contains nodes ordered as shortest path
    '''
    node = end_node
    path = []
    while node.station_name != start_node.station_name:
        path.append(node)
        node = previous_node[node]
    path.reverse()
    path.insert(0, start_node)
    return path


def find_nearest(nodes_list, cost_dict):
    '''
    find index of the nearest node (from start_node) in a list of nodes
    @param nodes_list: a list of all considering nodes
    @param cost_dict: a dictionary showing cost from start node to a particular
                      node, formed : {node_x: cost_x}
    @return nearest_index: index of the nearest node
    '''
    nearest_index = 0
    min_cost = cost_dict[nodes_list[nearest_index]]
    for index, node in enumerate(nodes_list):
        if cost_dict[node] < min_cost:
            nearest_index = index
    return nearest_index


def implement_dijkstra(start_node, end_node, all_nodes_list, cost_dict):
    '''
    implement dijkstra's algorithm to find the shortest path between start and
    end node
    @param start_node: the start station of trains
    @param end_node: the destination of the trains
    @param all_nodes_list: a dictionary showing cost from start node to a
                       particular node, formed : {node_x: cost_x}
    @param cost_dict: a dictionary showing cost from start node to a particular
                      node, formed : {node_x: cost_x}
    @return: - a list contains nodes ordered as shortest path
             - an empty list if there is no any path
    '''
    previous_node = {}
    open_list = [start_node]
    close_list = []
    while open_list:
        nearest_index = find_nearest(open_list, cost_dict)
        current_node = open_list.pop(nearest_index)
        close_list.append(current_node)
        # terminating condition
        if current_node == end_node:
            return track_back(start_node, end_node, previous_node)
        # extend new nodes from current_node
        new_nodes_list = find_new_nodes(current_node, all_nodes_list)
        if not new_nodes_list:
            continue
        # validate new nodes then add them to open_list
        open_list = validate_new_nodes(current_node, new_nodes_list,
                                       close_list, open_list, previous_node,
                                       cost_dict)
    return []


def init_cost_dict(start_node, all_nodes_list):
    '''
    initialize a dictionary contains all of nodes as key and value of each key
    cost from the start_node to that node. initiated value = infinity
    @param start_node: the start station of trains
    @param all_nodes_list: a list of all nodes in graph
    @return cost_dict: a dictionary showing cost from start node to a
                       particular node, formed : {node_x: cost_x}
    '''
    cost_dict = {}
    for node in all_nodes_list:
        if node == start_node:
            cost_dict[node] = 0
        else:
            cost_dict[node] = inf
    return cost_dict


def get_nodes_list(nodes_dict):
    '''
    create a list contains all of the nodes in graph
    @param nodes_dict: dictionary contains node_name as key and value is
                       node object
    @return all_nodes_list: a list of all nodes in graph
    '''
    all_nodes_list = []
    for node in nodes_dict:
        all_nodes_list.append(nodes_dict[node])
    return all_nodes_list


def find_all_path(start_node, end_node, nodes_dict):
    '''
    find all of available paths from start node to end node without any common
    node
    @param start_node: the start station of trains
    @param end_node: the destination of the trains
    @param nodes_dict: dictionary contains node_name as key and value is
                       node object
    @param cost_dict: a dictionary showing cost from start node to a particular
                      node, formed : {node_x: cost_x}
    @return paths_list: a list contains all of paths which are lists contains
                    nodes ordered as shortest path
    '''
    all_nodes_list = get_nodes_list(nodes_dict)
    paths_list = []
    while True:
        cost_dict = init_cost_dict(start_node, all_nodes_list)
        path = implement_dijkstra(start_node, end_node,
                                  all_nodes_list, cost_dict)
        if path:
            paths_list.append(path)
            for node in path[1:-1]:
                all_nodes_list.remove(node)
        else:
            break
    return paths_list
