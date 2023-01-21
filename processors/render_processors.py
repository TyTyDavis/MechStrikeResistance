from math import floor
from esper import Processor
import tcod

from components import components


class CameraProcessor(Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        camera = self.world.camera
        playerx, playery = self.world.player_coordinates()
        
        camera.update(playerx, playery, self.world.zoomed_out)

class MapRenderProcessor(Processor):
    def __init__(self):
        super().__init__()

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
        #print messages one line at a time
        #y = self.world.message_log.y
        #for message in self.world.message_log.messages:
        #    tcod.console_set_default_foreground(panel, message.color)
        #    tcod.console_print_ex(panel, self.world.message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
        #    y +=1
        #replace tens with fuel variables
        #self.render_bar(panel, 1, 1,self.world.bar_width, '', 10, 10, tcod.light_red, tcod.dark_red)
        #tcod.console_blit(panel, 0, 0, self.world.screen_width, self.world.panel_height, 0, self.world.panel_x, self.world.panel_y)

class ClearProcessor(Processor):
    def __init__(self):
        super().__init__()

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
    def __init__(self):
        super().__init__()


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
                    con.print(x=coord[0] - camera.x, y=coord[1] - camera.y, string=render.chars[char_count][0], fg=render.chars[char_count][1])
                    char_count += 1
                    

                    

                