from esper import Processor
from math import floor
import sys
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
                coordinates.coordinates = self.move_coordinates(coordinates.coordinates, velocity.x, velocity.y)
                velocity.x = 0
                velocity.y = 0


class PlayerProcessor(Processor):
    def __init__(self):
        super().__init__()
    def process(self):
        if move := self.world.action.get("move"):
            for ent, (velocity, _) in self.world.get_components(components.Velocity, components.Player):
                    velocity.x = move[0]
                    velocity.y = move[1]
        
        elif self.world.action.get("embark"):
            
            if self.world.zoomed_out:
                self.world.zoomed_out = False
            else:
                self.world.zoomed_out = True
            #TODO: I don't like that the player processor handles this
            # The zoom should be some sort of event that gets sent game-wide
            self.world.camera.toggle_zoom(self.world.zoomed_out)

class Console(Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):

        if self.world.action.get('exit'):
            sys.exit()