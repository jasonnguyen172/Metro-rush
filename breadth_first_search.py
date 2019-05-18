def implement_bfs(start_node, end_node):
    open_list = [start_node]
    close_list = []
    came_from = {}
    while open_list:
        current_node = open_list.pop(0)
        new_nodes_list = current_node.neihgbours[:]
        close_list += [current_node]
        if not new_nodes_list:
            continue
        for new_node in new_nodes_list:
            if new_node in open_list:
                continue
            came_from[new_node] = current_node
            if new_node.station_name == end_node.station_name:
                return recontruct_path_bfs(start_node, end_node, came_from)
            open_list.append(new_node)


def recontruct_path_bfs(start_node, end_node, came_from):
    '''
    track back the path from goal
    '''
    node = end_node
    path = []
    while node.station_name != start_node.station_name:
        path.append(node)
        node = came_from[node]
    path.append(node)
    path.reverse()
    return path
