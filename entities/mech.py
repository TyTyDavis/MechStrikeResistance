from enum import Enum
from entities.entity import Entity
from characters import Characters



class Mech(Entity):
    def __init__(self, x, y, color, name, size=3, char=Characters.UP.value, face=Facing.NORTH, blocks=True):
        super().__init__(x, y, char, color, name, size, blocks)

    def update_coordinates(self):
        self.coordinates = []
        for x in range(self.x, self.x+self.size):
            for y in range(self.y, self.y+self.size):
                self.coordinates.append((x,y))
