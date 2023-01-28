from collections import Counter
from math import floor
import numpy
from scipy import stats

from tcod.console import Console

from map import tile_types
from render_functions import (
    screen_width, 
    screen_height,
    map_width, 
    map_height, 
    map_view_width, 
    map_view_height
)


class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = numpy.full((width, height), fill_value=tile_types.ground, order="F")
        self.zoomed_out_tiles = numpy.full((floor(self.width/3), floor(self.height/3)), fill_value=tile_types.ground, order="F")
        

        #test environment
        self.tiles[20:38, 20] = tile_types.wall
        self.tiles[20, 20:38] = tile_types.wall
        self.tiles[38, 20:38] = tile_types.wall
        self.tiles[20:28, 38] = tile_types.wall
        self.tiles[31:39, 38] = tile_types.wall
        self.tiles[21:38, 21:38] = tile_types.floor
        self.tiles[28:31, 38] = tile_types.floor

        

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height


    def average_of_tiles(self, tiles):
        tile = numpy.where(tiles["tile_type"]== 101)
        if tile[0].size > 0:
            return tiles[tile[0][0], tile[1][0]]
        else:
            #would prefer to return the mode tile type, but if above we are (eventually) checking for
            #"important" tiles, then taking the middle tile should be harmless
            return tiles[1][1]


    def create_zoomed_out_map(self):
        for x in range(0,map_width, 3):
            for y in range(0, map_height, 3):
                tiles = self.tiles[x:x+3, y:y+3]
                self.zoomed_out_tiles[floor(x/3), floor(y/3)] = self.average_of_tiles(tiles)


    def render_zoomed_in(self, console: Console, camerax, cameray) -> None:
        sliced_map = self.tiles[camerax:camerax+map_view_width, cameray:cameray+map_view_height]
        console.tiles_rgb[0:map_view_width, 0:map_view_height] = sliced_map["graphic"]
    
    def render_zoomed_out(self, console: Console) -> None:
        console.tiles_rgb[0:map_view_width, 0:map_view_height] = self.zoomed_out_tiles["graphic"]