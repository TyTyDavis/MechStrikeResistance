from typing import Tuple
import numpy

import tcod

from render_functions import Characters

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = numpy.dtype(
    [
        ("ch", numpy.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = numpy.dtype(
    [
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("graphic", graphic_dt),  # Graphics for when this tile is not in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    graphic: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> numpy.ndarray:
    """Helper function for defining individual tile types """
    return numpy.array((walkable, transparent, graphic), dtype=tile_dt)


ground = new_tile(
    walkable=True, transparent=True, graphic=(ord(Characters.MEDIUM_SHADE.value), tcod.black, tcod.darker_green),
)
wall = new_tile(
    walkable=False, transparent=False, graphic=(ord(" "), tcod.white, tcod.light_grey),
)