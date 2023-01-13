from esper import Processor
from math import floor
import tcod

from components import components

class MovementProcessor(Processor):
    def __init__(self):
        super().__init__()

    def move_coordinates(self, coordinates, velocityx, velocityy):
        new_coords = []
        for coord in coordinates:
            new_coords.append((coord[0] + velocityx, coord[1] + velocityy))
        return new_coords

    def process(self):
        for ent, (velocity, coordinates) in self.world.get_components(components.Velocity, components.Coordinates):
            if velocity.x or velocity.y:
                #import pdb; pdb.set_trace()
                coordinates.coordinates = self.move_coordinates(coordinates.coordinates, velocity.x, velocity.y)
                print(coordinates)


class PlayerProcessor(Processor):
    def __init__(self):
        super().__init__()
    def process(self):
        for ent, (velocity, _) in self.world.get_components(components.Velocity, components.Player):
            if move := self.world.action.get("move"):
                velocity.x = move[0]
                velocity.y = move[1]
            else:
                velocity.x = 0
                velocity.y = 0