from enum import Enum
from entities.entity import Entity
from render_functions import Characters

class Facing(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"


class Mech(Entity):
    def __init__(self, x, y, color, name, char=Characters.UP.value, face=Facing.NORTH, blocks=True):
        self.size = 3
        super().__init__(x, y, char, color, name, self.size, blocks)