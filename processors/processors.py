from esper import Processor
from math import floor
import sys
import tcod

from components import components
from characters import Characters, CHARACTER_MAPPINGS

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
            self.world.game_map.create_zoomed_out_map()
            self.world.camera.toggle_zoom(self.world.zoomed_out)


def determine_rendered_facing(chars):
    center_char = chars[4][0]
    if center_char == Characters.UP_POINTING_TRIANGLE.value:
        return components.Directions.NORTH.value
    elif center_char == Characters.DOWN_POINTING_TRIANGLE.value:
        return components.Directions.SOUTH.value
    elif center_char == Characters.RIGHT_POINTING_TRIANGLE.value:
        return components.Directions.EAST.value
    elif center_char == Characters.LEFT_POINTING_TRIANGLE.value:
        return components.Directions.WEST.value

def get_character_list(char):
    for key, list in CHARACTER_MAPPINGS.items():
        if char in list:
            return list
        
class MechProcessor(Processor):
    def __init__(self):
        super().__init__()
    
    

    def rotations_needed(self, start, end):
        directions = [components.Directions.NORTH.value, components.Directions.EAST.value, components.Directions.SOUTH.value, components.Directions.WEST.value]
        start_index = directions.index(start)
        end_index = directions.index(end)
        rotations = (start_index - end_index) % 4
        return rotations
    
    def rotated_mech_render(self, chars, rendered_facing, true_facing):
        new_chars = chars
        rotations_needed = self.rotations_needed(rendered_facing, true_facing)
        for _ in range(rotations_needed):
            new_chars = [
                new_chars[6],
                new_chars[3],
                new_chars[0],
                new_chars[7],
                new_chars[4],
                new_chars[1],
                new_chars[8],
                new_chars[5],
                new_chars[2],
            ]
        for x in range(len(new_chars)):
            if char_list:=get_character_list(new_chars[x][0]):
                character= char_list[(char_list.index(new_chars[x][0]) + rotations_needed) % 4]
                new_chars[x] = (character, new_chars[x][1])

        return new_chars
        


    def process(self):
        for ent, (mech, render) in self.world.get_components(components.Mech, components.Render):
            rendered_facing = determine_rendered_facing(render.chars)
            if rendered_facing != mech.facing:
                render.chars = self.rotated_mech_render(render.chars, rendered_facing, mech.facing)


class Console(Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def process(self):

        if self.world.action.get('exit'):
            sys.exit()