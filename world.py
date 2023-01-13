import esper
import tcod

from components import components
from game_messages import MessageLog
from map_objects.game_map import GameMap
from render_functions import Camera

class World(esper.World):
    
    def __init__(self, con, panel):
        super().__init__()
        self.zoomed_out = False

        self.map_view_width = 63
        self.map_view_height = 63

        self.map_width = self.map_view_width * 3
        self.map_height = self.map_view_height *3

        self.panel_width = 20
        self.panel_height = self.map_view_height

        self.screen_width = self.map_view_width + self.panel_width
        self.screen_height = self.map_view_height

        self.panel_x = self.screen_width - self.panel_width
        self.panel_y = self.screen_height - self.panel_height	

        self.bar_width = 15

        self.message_x = 1
        self.message_y = 5
        self.message_width = 20
        self.message_height = 40

        self.message_log = MessageLog(self.message_x, self.message_y, self.message_width, self.message_height)
        self.game_map = GameMap(self.map_view_width * 3 , self.map_view_height * 3)
        self.game_map.make_map(self.map_view_width, self.map_view_height)

        self.camera = Camera(63+1, 63+1)
        self.con = con
        self.panel = panel
        
        self.colors = {
            'dark_wall': tcod.Color(0, 0, 100),
            'dark_ground': tcod.Color(50, 50, 150),
            'light_wall': tcod.darkest_blue,
            'light_ground': tcod.desaturated_blue
	    }
        self.action = {}

    def player_coordinates(self):
        for player, (player, coordinates) in self.get_components(components.Player, components.Coordinates):
            return coordinates.coordinates[0]
        return False