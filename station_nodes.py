class Node:

    def __init__(self, station_name, station_id, connected=False):
        self.station_name = station_name
        # station_id: a dict with key= line and value= ID
        # exp: {line1: id1, line2: id2}
        self.station_id = station_id
        self.connected = connected
        self.neihgbours = None
        self.trains = []


class Trains:

    def __init__(self, graph, station_node, train_name, stay=   False):
        self.train_name = train_name
        self.stay = stay
        station_node.trains.append(self)
