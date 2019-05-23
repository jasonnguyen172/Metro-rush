#! /usr/bin/env python3
import pyglet
from pyglet.window import key, mouse
from pyglet.gl import *


class Node_coordinate():
    def __init__(self, coordinate_tuple):
        self.coordinate = []  # list of tuples storing station's coordinate
        self.coordinate.append(coordinate_tuple)


class GUI(pyglet.window.Window):
    def __init__(self, graph, data_gui, screen, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph = graph  # a Graph's object
        self.all_nodes = {}
        (self.coordinate_data,
         self.station_data) = generate_lines_coordinate(graph, screen, self)
        self.current_turn = 0
        self.data_gui = data_gui  # data for visualizing purpose
        self.train_image = pyglet.resource.image("train.png")
        self.start_image = pyglet.resource.image("start.png")
        self.end_image = pyglet.resource.image("end.png")
        # add turn 0 to the data set
        self.data_gui.insert(0, [data_gui[0][0]])

    def on_draw(self):
        """
        Draw on screen based on given data
        This function will be called each turn
        """
        self.clear()

        ####################### Draw lines and stations ########################
        for data in self.coordinate_data:
            temp = self.coordinate_data[data]
            # draw line
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,('v2i', (temp[0], temp[1], temp[2], temp[3])),('c3B', (240, 128, 128, 240, 128, 128)))
            # draw line's name
            temp[4].draw()
            # draw stations on line
            for index, sprite in enumerate(temp[5]):
                sprite.draw()
                label = pyglet.text.Label(temp[6][index],
                                  font_name='Times New Roman',
                                  font_size=12,
                                  anchor_x='right', anchor_y='top')
                # draw station's name with an angle of 50 degree
                glPushMatrix()
                glLoadIdentity()
                glTranslatef(temp[7][index][0], temp[7][index][1] - 5, 0.0)
                glRotatef(50.0, 0.0, 0.0, 1.0)
                label.draw()
                glRotatef(-50.0, 0.0, 0.0, 1.0)
                glPopMatrix()

        ####################### Draw connected lines ###########################
        for node in self.all_nodes:
            if len(self.all_nodes[node].coordinate) > 1:
                for index, coordinate in enumerate(self.all_nodes[node].coordinate):
                    # find and match connected stations by a grey line
                    try:
                        current = self.all_nodes[node].coordinate[index]
                        next = self.all_nodes[node].coordinate[index + 1]
                        # draw grey lines
                        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,('v2i', (current[0] + 6, current[1] + 6, next[0] + 6, next[1] + 6)),('c3B', (54, 54, 54, 54, 54, 54)))
                    except IndexError:
                        pass

        ####################### Draw start-end station #########################
        # find start/end station's name/line, in order to get it's coordinates
        end_station = self.data_gui[-1][-1].split("(")[0]
        start_station = self.data_gui[0][0].split("(")[0]
        end_line = (self.data_gui[-1][-1].split("(")[1]).split(":")[0]
        start_line = (self.data_gui[0][0].split("(")[1]).split(":")[0]
        (end_x, end_y) = self.station_data[end_line][end_station]
        (start_x, start_y) = self.station_data[start_line][start_station]
        # draw symbols over those stations
        for x_position, y_position, image in [(end_x - 6, end_y - 30, self.end_image),
                                              (start_x - 6, start_y + 20, self.start_image)]:
            pyglet.sprite.Sprite(image, x=x_position, y=y_position).draw()

        ########################### Draws trains ###############################
        for line in self.data_gui[self.current_turn]:
            # get station's name and line
            station_name = line.split("(")[0]
            station_line = (line.split("(")[1]).split(":")[0]
            # get station's coordinate
            (station_x, station_y) = self.station_data[station_line][station_name]
            # draw trains
            pyglet.sprite.Sprite(self.train_image, x=station_x - 6, y=station_y - 6).draw()

    ########################## Control user's action ###########################
    def on_key_press(self, symbol, modifiers):
        """
        Go next/ previous turn depend on key pressed
        """
        if symbol == key.LEFT and (self.current_turn - 1 >= 0):
            self.current_turn -= 1
        elif symbol == key.RIGHT and (self.current_turn + 1 < len(self.data_gui)):
            self.current_turn += 1

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Go next/ previous turn depend on mouse pressed
        """
        if button == mouse.RIGHT and (self.current_turn - 1 >= 0):
            self.current_turn -= 1
        elif button == mouse.LEFT and (self.current_turn + 1 < len(self.data_gui)):
            self.current_turn += 1


def generate_lines_coordinate(graph, screen, gui):
    def generate_coordinate_data(line, list_sprite, stations,
                                 positions):
        """
        Create data about station/ line's coordinates and store them
        In order to draw later

        @param: list_sprite, stations, positions: empty list
        """
        for index, station in enumerate(graph.lines_dict[line]):
            image = pyglet.resource.image("station.png")
            if station.connected:
                image = pyglet.resource.image("interchange.png")
            # set coordinate automatically base on station index
            # and screen size
            sprite_x = int(((screen.width*0.85) / station_number) * index + start_x_coordinate)
            sprite_y = start_y_coordinate - 6
            # store the sprite's coordinates if the station already the dict
            if station in gui.all_nodes:
                gui.all_nodes[station].coordinate.append((sprite_x, sprite_y))
            # else, update
            else:
                gui.all_nodes[station] = Node_coordinate((sprite_x, sprite_y))
            sprite = pyglet.sprite.Sprite(image, x=sprite_x , y=sprite_y)
            # store all station's sprites
            list_sprite.append(sprite)
            # store all station's names
            stations.append(station.station_name)
            # store their coordinates
            positions.append((sprite_x, sprite_y))
            # store the coordinates if the station already the dict
            if line not in station_data:
                station_data[line] = {station.station_name:(sprite_x, sprite_y)}
            else:
                station_data[line][station.station_name] = (sprite_x, sprite_y)

        return (start_x_coordinate, start_y_coordinate,
                end_x_coordinate, start_y_coordinate,
                label, list_sprite, stations, positions)

    line_number = len(graph.lines_dict)
    coordinate_data, station_data = dict(), dict()

    for index, line in enumerate(graph.lines_dict.keys()):
        # automatically generate start/ end point of a line
        # in oder to draw that line
        start_x_coordinate = int(screen.width*0.1)
        start_y_coordinate = int((screen.height*0.9 / line_number) * (index + 1.5))
        end_x_coordinate = int(screen.width*0.95)
        # line's name
        label = pyglet.text.Label(line,
                          font_name='Times New Roman',
                          font_size=15,
                          x=screen.width*0.05, y=start_y_coordinate,
                          anchor_x='center', anchor_y='center', color=(0, 206, 209, 255))
        list_sprite, stations, positions = list(), list(), list()
        # find the number of station
        station_number = len(graph.lines_dict[line])
        coordinate_data[line] = generate_coordinate_data(line,
                                                         list_sprite, stations,
                                                         positions)

    return (coordinate_data, station_data)


def get_screen():
    """
    Return all current-screen's useful information
    """
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    return display.get_default_screen()


def display(graph, data_gui):
    screen = get_screen()
    # create a full screen window
    gui = GUI(graph, data_gui, screen, screen.width, screen.height, 'GUI')
    pyglet.app.run()


if __name__ == "__main__":
    display()
