from math import floor
from esper import Processor
import tcod

from components import components
from visuals import colors


class CameraProcessor(Processor):
    def process(self):
        camera = self.world.camera
        playerx, playery = self.world.player_coordinates()
        
        camera.update(playerx, playery, self.world.zoomed_out)

class MapRenderProcessor(Processor):
    def render_bar(self, panel, x, y, total_width, name, value, maximum, bar_color, back_color):
        bar_width = int(float(value) / maximum * total_width)
        tcod.console_set_default_background(panel, back_color)
        tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)
		
        tcod.console_set_default_background(panel, bar_color)
		
        if bar_width > 0:
            tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)
			
        tcod.console_set_default_foreground(panel, tcod.white)
        tcod.console_print_ex(panel, int(x + total_width / 2), y, tcod.BKGND_NONE, tcod.CENTER, '{0}: {1}/{2}'.format(name, value, maximum))


    def process(self):
        con = self.world.con
        camera = self.world.camera
        panel = self.world.panel

        zoom_factor = 1
        if self.world.zoomed_out:
            self.world.game_map.render_zoomed_out(con)
        else:
            self.world.game_map.render_zoomed_in(con, camera.x, camera.y)
		
        #render HUD
        tcod.console_set_default_background(panel, tcod.black)
        tcod.console_clear(panel)
        
class HUDProcessor(Processor):
    def render_bar(self, panel, x, y, total_width, name, value, maximum, bar_color, text_color):
        bar_width = int(float(value) / maximum * total_width)
        panel.draw_rect(x=x, y=y, width=bar_width, height=1, ch=1, fg=None, bg=bar_color)
			
        value_string = f"{value}/{maximum}"
        panel.print(x=int(x + total_width - len(value_string)), y=y, string=value_string, fg=text_color)
        panel.print(x=x, y=y, string=name, fg=text_color)
    
    def process(self):
        panel = self.world.panel
        
        for entity, (inventory, hitpoints, player) in self.world.get_components(components.Inventory, components.HitPoints, components.Player):
            money = inventory.money
            hp = hitpoints.hp
            maxHP = hitpoints.maxHP


        #UI 
        panel.draw_frame(x=0, y=31, width=20, height=32, fg=colors.ui_green)
        
        #bars

        self.render_bar(panel, 1, 1, 18, "HP", hp, maxHP, tcod.red, tcod.white)

        #text values
        panel.print(x=1, y=3, string=f"$:{money}", fg=colors.ui_green)  

        #messages
        y = self.world.message_log.y
        for message in self.world.message_log.messages:
            #import pdb; pdb.set_trace()
            panel.print(x=self.world.message_log.x, y=y, string=message.text, fg=message.color)      
            y +=1

class ClearProcessor(Processor):

    def process(self):
        con = self.world.con
        camera = self.world.camera

        zoom_factor = 1
        if self.world.zoomed_out:
            zoom_factor = 3

        
        for entity, (coordinates, render) in self.world.get_components(components.Coordinates, components.Render):
            if self.world.zoomed_out:
                tcod.console_set_default_foreground(con, render.chars[0][1])
                tcod.console_put_char(con, floor(coordinates.coordinates[0][0]/zoom_factor), floor(coordinates.coordinates[0][1]/zoom_factor)," ", tcod.BKGND_NONE)
            else:
                for coord in coordinates.coordinates:
                    tcod.console_set_default_foreground(con, render.chars[0][1])
                    con.print(x=coord[0] - camera.x, y=coord[1] - camera.y, string=" ")


class EntityRenderProcessor(Processor):
    def process(self):
        con = self.world.con
        camera = self.world.camera

        zoom_factor = 1
        if self.world.zoomed_out:
            zoom_factor = 3
        if self.world.zoomed_out:
            for entity, (coordinates, render, _) in self.world.get_components(components.Coordinates, components.Render, components.RenderZoomedOut):
                con.print(
                    x=floor(coordinates.coordinates[0][0]/zoom_factor), 
                    y=floor(coordinates.coordinates[0][1]/zoom_factor), 
                    string=render.chars[4][0], 
                    fg=render.chars[4][1]
            )
        else:
            for entity, (coordinates, render) in self.world.get_components(components.Coordinates, components.Render):
                char_count = 0
                for coord in coordinates.coordinates:
                    con.print(
                        x=coord[0] - camera.x, 
                        y=coord[1] - camera.y, 
                        string=render.chars[char_count][0] if len(render.chars) > char_count else ' ', 
                        fg=render.chars[char_count][1] if len(render.chars) > char_count else None
                    )
                    char_count += 1
                    

                    

                