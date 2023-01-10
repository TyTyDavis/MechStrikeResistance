from esper import Processor
from math import floor
import tcod

from components import components

class MovementProcessor(Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (velocity, coordinates) in self.world.get_components(components.Velocity, components.Coordinates):
            if velocity.x or velocity.y:
                for coord in coordinates:
                    coord[0] += velocity.x
                    coord[1] += velocity.y

class ZoomedInRenderProcessor(Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for entity, (coordinates,render) in self.world.get_components(components.Coordinates, components.RenderZoomedIn): 
            for coord in coordinates:
                tcod.console_put_char(
                    self.con, 
                    floor(coord[0]/self.zoom_factor), 
                    floor(coord[1]/self.zoom_factor), 
                    render.chars[0][0], 
                    tcod.BKGND_NONE
                )
