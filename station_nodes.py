class Node:

    def __init__(self, station_name, station_id, connected=False):
        self.station_name = station_name
        # station_id: a dict with key= line and value= ID
        # exp: {line1: id1, line2: id2}
        self.station_id = station_id
        self.connected = connected
        self.neihgbours = None