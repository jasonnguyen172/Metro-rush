class Node:
    """
    Store all informations of one station
    """
    def __init__(self, station_name, station_id, connected=False):
        self.station_name = station_name
        # station_id: a dict with key= line and value= ID
        # exp: {line1: id1, line2: id2}
        self.station_id = station_id
        self.connected = connected
        # a list, which store all neihgbour stations of this station
        self.neihgbours = []
        # a list, which store all trains that are on this station
        self.trains = []


class Train:
    """
    Store all information of one train
    """
    def __init__(self, current_line, start_node, train_name, stay=False):
        self.train_name = train_name
        # default = False, turn True if train need to stop,
        self.stay = stay
        self.current_line = current_line
        # add train instance to start node
        start_node.trains.append(self)
