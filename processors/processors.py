from esper import Processor
from math import floor
import sys
import tcod

from components import components
from visuals.characters import Characters, CHARACTER_MAPPINGS



def do_coordinates_overlap(coordinates_1, coordinates_2):
    return bool(set(coordinates_1) & set(coordinates_2))

class MovementProcessor(Processor):
    def __init__(self):
        super().__init__()

    def get_blocking_entities_at_location(self, actor_ent, actor_coordinates, with_mech):
        for ent, (coordinates, collision) in self.world.get_components(components.Coordinates, components.Collision):
            if do_coordinates_overlap(actor_coordinates, coordinates.coordinates) and ent != actor_ent:
                if with_mech == False and self.world.has_component(ent, components.Mech):
                    return None
                return ent
        return None
    
    def move_coordinates(self, raw_coordinates, velocityx, velocityy):
        new_coords = []
        for coord in raw_coordinates:
            new_coords.append((coord[0] + velocityx, coord[1] + velocityy))
        for coord in new_coords:
            if self.world.game_map.tiles["blocked"][coord[0], coord[1]]:
                return raw_coordinates
        return new_coords

    def process(self):
        player_ent, player = self.world.get_component(components.Player)[0]
        for ent, (velocity, coordinates, moves, collision) in self.world.get_components(components.Velocity, components.Coordinates, components.Moves, components.Collision):
            if velocity.x or velocity.y:
                velocity.x, velocity.y = tuple(v * moves.speed for v in (velocity.x, velocity.y))
                
                new_coordinates = self.move_coordinates(coordinates.coordinates, velocity.x, velocity.y)
                #if target := self.get_blocking_entities_at_location(ent, new_coordinates, collision.with_mech):
                #    self.world.message_log.add_message("Attack!")
                #else:
                coordinates.coordinates = new_coordinates

                if ent == player.vehicle:
                    player_coordinates = self.world.component_for_entity(player_ent, components.Coordinates)
                    player_coordinates.coordinates = [coordinates.coordinates[4]]
                
                velocity.x = 0
                velocity.y = 0


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
        rotations = (end_index - start_index) % 4
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
            if mech.embarked:
                if face := self.world.action.get("face"):
                    mech.facing = face
            
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