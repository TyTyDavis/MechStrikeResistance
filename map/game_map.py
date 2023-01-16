import numpy
from tcod.console import Console

from map import tile_types
from render_functions import screen_width, screen_height


class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = numpy.full((width, height), fill_value=tile_types.ground, order="F")

        self.tiles[30:33, 22] = tile_types.wall

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render_zoomed_in(self, console: Console, camerax, cameray) -> None:
        sliced_map = self.tiles[camerax:camerax+screen_width, cameray:cameray+screen_height]
        console.tiles_rgb[0:screen_width, 0:screen_height] = sliced_map["graphic"]