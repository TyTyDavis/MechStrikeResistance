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
        if self.world.zoomed_out:
            camera.x, camera.y = (0,0)
        if playerx < camera.x + camera.border and camera.x >= 0:
            camera.x -= 1
        elif playerx > camera.x + self.world.map_view_width - camera.border and camera.x <= self.world.map_width:
            camera.x += 1
        elif playery < camera.y + camera.border and camera.y >= 0:
            camera.y -= 1
        elif playery > camera.y + self.world.map_view_height - camera.border and camera.y <= self.world.map_height:
            camera.y += 1

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
            zoom_factor = 3
        for y in range(self.world.map_view_height):
            for x in range(self.world.map_view_width):
                wall = self.world.game_map.tiles[camera.x + x][camera.y + y].block_sight	
                if wall:
                    tcod.console_set_char_background(con, floor(x/zoom_factor), floor(y/zoom_factor), self.world.colors.get('light_wall'), tcod.BKGND_SET)
                else:
                    tcod.console_set_char_background(con, floor(x/zoom_factor), floor(y/zoom_factor), self.world.colors.get('light_ground'), tcod.BKGND_SET)	
		
        tcod.console_blit(con, 0, 0, self.world.screen_width, self.world.screen_height, 0, 0, 0)
		
        #render HUD
        tcod.console_set_default_background(panel, tcod.black)
        tcod.console_clear(panel)
        #print messages one line at a time
        y = self.world.message_log.y
        for message in self.world.message_log.messages:
            tcod.console_set_default_foreground(panel, message.color)
            tcod.console_print_ex(panel, self.world.message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
            y +=1
            
        #replace tens with fuel variables
        self.render_bar(panel, 1, 1,self.world.bar_width, '', 10, 10, tcod.light_red, tcod.dark_red)
        tcod.console_blit(panel, 0, 0, self.world.screen_width, self.world.panel_height, 0, self.world.panel_x, self.world.panel_y)

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
                tcod.console_put_char(con, floor(coordinates[0][0]/zoom_factor), floor(coordinates[0][1]/zoom_factor)," ", tcod.BKGND_NONE)
            else:
                for coord in coordinates.coordinates:
                    tcod.console_set_default_foreground(con, render.chars[0][1])
                    tcod.console_put_char(con, coord[0] - camera.x, coord[1] - camera.y, " ", tcod.BKGND_NONE)
class EntityRenderProcessor(Processor):
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
                tcod.console_put_char(con, floor(coordinates[0][0]/zoom_factor), floor(coordinates[0][1]/zoom_factor), render.chars[0][0], tcod.BKGND_NONE)
            else:
                for coord in coordinates.coordinates:
                    tcod.console_set_default_foreground(con, render.chars[0][1])
                    tcod.console_put_char(con, coord[0] - camera.x, coord[1] - camera.y, render.chars[0][0], tcod.BKGND_NONE)

            