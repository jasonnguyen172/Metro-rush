from functions import *
from math import inf


def calculate_cost(shortest_path, graph):
    '''
    compute cost of a completed path
    @param shortest_path: type: list -a list contains nodes ordered as
                          completed shortest path
    return cost: int number - cost of shortest path
    '''
    cost = get_edge(shortest_path[0], shortest_path[1], graph)
    if len(shortest_path) > 2:
        previous_line = get_common_line(shortest_path[0], shortest_path[1])
        for index, node in enumerate(shortest_path[2:], 2):
            edge = get_edge(shortest_path[index-1], node, graph)
            try:
                if get_common_line(shortest_path[index-1], node) != \
                 previous_line:
                    edge += 1
                cost += edge
                previous_line = get_common_line(shortest_path[index-1], node)
            except TypeError:
                print('the shortest path was lack of one node or more')
                return
    return cost


def validate_new_nodes(graph, current_node, new_nodes_list, close_list,
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
            # track back the route from start node to new node
            old_previous_node = previous_node[new_node]
            previous_node[new_node] = current_node
            temporary_route = track_back(graph.start_node, new_node,
                                         previous_node)
            if calculate_cost(temporary_route, graph) >= cost_dict[new_node]:
                # reset the previous node
                previous_node[new_node] = old_previous_node
                continue
        # set information for validated new node
        previous_node[new_node] = current_node
        cost_dict[new_node] = calculate_cost(
         track_back(graph.start_node, new_node, previous_node), graph)
        open_list.append(new_node)
    return open_list


def find_new_nodes(current_node, all_nodes_list):
    '''
    extend all neihgbour nodes from a current node for the next considered
    nodes
    @parram current_node: the current considered node
    @param all_nodes_list: a list of all nodes in graph
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


def find_nearest(open_list, cost_dict):
    '''
    find index of the nearest node (from start_node) in a list of nodes
    @param open_list: a list of all considering nodes
    @param cost_dict: a dictionary showing cost from start node to a particular
                      node, formed : {node_x: cost_x}
    @return nearest_index: index of the nearest node
    '''
    nearest_index = 0
    min_cost = cost_dict[open_list[nearest_index]]
    for index, node in enumerate(open_list):
        if cost_dict[node] < min_cost:
            nearest_index = index
    return nearest_index


def execute_dijkstra(graph, all_nodes_list, cost_dict):
    '''
    implement dijkstra's algorithm to find the shortest path between start and
    end node
    @param start_node: the start station of trains
    @param end_node: the destination of the trains
    @param all_nodes_list: a list of all nodes in graph
    @param cost_dict: a dictionary showing cost from start node to a particular
                      node, formed : {node_x: cost_x}
    @return: - a list contains nodes ordered as shortest path
             - an empty list if there is no any path
    '''
    previous_node = {}
    open_list = [graph.start_node]
    close_list = []
    while open_list:
        nearest_index = find_nearest(open_list, cost_dict)
        current_node = open_list.pop(nearest_index)
        close_list.append(current_node)
        # terminating condition
        if current_node == graph.end_node:
            return track_back(graph.start_node, graph.end_node, previous_node)
        # extend new nodes from current_node
        new_nodes_list = find_new_nodes(current_node, all_nodes_list)
        if not new_nodes_list:
            continue
        # validate new nodes then add them to open_list
        open_list = validate_new_nodes(
            graph, current_node, new_nodes_list, close_list,
            open_list, previous_node, cost_dict)
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


def find_all_paths(graph):
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
    all_nodes_list = get_nodes_list(graph.nodes_dict)
    routes_list = []
    finished_route_list = []
    while True:
        cost_dict = init_cost_dict(graph.start_node, all_nodes_list)
        route = execute_dijkstra(graph, all_nodes_list, cost_dict)
        finished_route = get_finished_route(graph, route, all_nodes_list)
        if finished_route:
            finished_route_list.append(format_route(finished_route))
            routes_list.append(route)
            for node in finished_route[1:-1]:
                all_nodes_list.remove(node)
        else:
            break
    return routes_list, finished_route_list


def format_route(finished_route):
    formated_route = []
    for index, node in enumerate(finished_route[:-1]):
        if node.connected and index > 0:
            line = get_common_line(finished_route[index-1], node)
            formated_route.append(format_node(node, line))
        line = get_common_line(finished_route[index+1], node)
        formated_route.append(format_node(node, line))
    line = get_common_line(finished_route[-1], finished_route[-2])
    formated_route.append(format_node(finished_route[-1], line))
    return formated_route


def format_node(node, line):
    formated_node = node.station_name + \
                    '(' + line + ':' + str(node.station_id[line]) + ')'
    return formated_node


def get_route_last_to_first(last_node, first_node, line, graph):
    last_node_index = last_node.station_id[line] - 1
    first_node_index = first_node.station_id[line] - 1
    lines_list = graph.lines_dict[line]
    length_line = len(lines_list)
    last_route = lines_list[last_node_index: length_line]
    first_route = lines_list[1: first_node_index + 1]
    return last_route + first_route


def get_route_first_to_last(last_node, first_node, line, graph):
    return get_route_last_to_first(last_node, first_node, line, graph)[::-1]


def check_cirle_move(source_node, dest_node, graph):
    line = get_common_line(source_node, dest_node)
    interchange_list = graph.interchange_dict[line]
    if line in graph.circular_lines_list:
        if abs(interchange_list.index(source_node) -
               interchange_list.index(dest_node)) > 1:
            return True
        elif len(interchange_list) == 2:
            return True
    return False


def get_info_of_source_node_dest_node(source_node, dest_node):
    line = get_common_line(source_node, dest_node)
    source_node_index = source_node.station_id[line] - 1
    dest_node_index = dest_node.station_id[line] - 1
    return source_node_index, dest_node_index, line


def get_route_of_cirle_move(source_node, dest_node, graph, all_nodes_list):
    source_node_index, dest_node_index, line =\
        get_info_of_source_node_dest_node(source_node, dest_node)
    interchange_list = graph.interchange_dict[line]
    if source_node_index > dest_node_index:
        last_node, first_node = source_node, dest_node
        route = get_route_last_to_first(last_node, first_node, line, graph)
    elif source_node_index < dest_node_index:
        last_node, first_node = dest_node, source_node
        route = get_route_first_to_last(last_node, first_node, line, graph)
    if len(interchange_list) == 2:

        normal_route = get_route_normal_move(source_node, dest_node,
                                             graph, all_nodes_list)
        if len(route) > len(normal_route):
            route = normal_route
    for node in route[1:-1]:
        if node not in all_nodes_list:
            return []
        else:
            return route
    return []


def get_route_normal_move(source_node, dest_node, graph, all_nodes_list):
    route = [source_node]
    line = get_common_line(source_node, dest_node)
    step = -1
    next_node = source_node
    index_next_node = graph.lines_dict[line].index(source_node)
    if source_node.station_id[line] < dest_node.station_id[line]:
        step = 1
    while next_node != dest_node:
        index_next_node += step
        next_node = graph.lines_dict[line][index_next_node]
        if next_node not in all_nodes_list:
            return []
        route.append(next_node)
    return route


def get_finished_route_two_nodes(source_node, dest_node, graph,
                                 all_nodes_list):

    if check_cirle_move(source_node, dest_node, graph):

        return get_route_of_cirle_move(source_node, dest_node, graph,
                                       all_nodes_list)
    else:
        return get_route_normal_move(source_node, dest_node, graph,
                                     all_nodes_list)


def get_finished_route(graph, temporary_route, all_nodes_list):
    finished_route = []
    for index, node in enumerate(temporary_route[1:], 1):
        finished_route += get_finished_route_two_nodes(
            temporary_route[index - 1], node, graph, all_nodes_list)[1:]
    if finished_route:
        finished_route.insert(0, graph.start_node)
    return finished_route
