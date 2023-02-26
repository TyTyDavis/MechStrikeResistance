from esper import Processor

from components import components
from processors.processors import do_coordinates_overlap

class PlayerProcessor(Processor):
    def __init__(self):
        super().__init__()
    

    def process(self):
        for player_ent, (player, player_coordinates) in self.world.get_components(components.Player, components.Coordinates):
            player.interactables = []
            for ent, (mech, coordinates) in self.world.get_components(components.Mech, components.Coordinates):
                if do_coordinates_overlap(player_coordinates.coordinates, coordinates.coordinates):
                    if not mech.occupied:
                        player.interactables.append(ent)
           
            if move := self.world.action.get("move"):
                for ent, (velocity, _) in self.world.get_components(components.Velocity, components.Controlled):
                        velocity.x = move[0]
                        velocity.y = move[1]
            
            elif self.world.action.get("embark"):
                for ent, (mech, controlled) in self.world.get_components(components.Mech, components.Controlled):
                    #disembark
                    mech.embarked = False
                    mech.occupied = False
                    player.vehicle = None
                    player_move = self.world.component_for_entity(player_ent, components.Moves)

                    self.world.add_component(player_ent, components.Controlled())
                    self.world.remove_component(ent, components.Controlled)

                    self.world.zoomed_out = False
                    self.world.camera.toggle_zoom(self.world.zoomed_out)
                    player.interactables = []
                for entity in player.interactables:
                    if self.world.has_component(entity, components.Mech):
                        mech = self.world.component_for_entity(entity, components.Mech)
                        mech_coords = self.world.component_for_entity(entity, components.Coordinates)
                        if not mech.occupied: #embark
                            mech.embarked = True
                            mech.occupied = True
                            player.vehicle = entity
                            player_move = self.world.component_for_entity(player_ent, components.Moves)
                            self.world.add_component(entity, components.Controlled())
                            self.world.remove_component(player_ent, components.Controlled)

                            self.world.zoomed_out = True
                            #TODO: I don't like that the player processor handles this
                            # The zoom should be some sort of event that gets sent game-wide
                            self.world.game_map.create_zoomed_out_map()
                            self.world.camera.toggle_zoom(self.world.zoomed_out)
            
            elif self.world.action.get("show_inventory"):
                self.world.message_log.add_message("Inventory empty")


