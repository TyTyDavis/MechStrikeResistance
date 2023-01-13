from math import floor
import tcod

from enum import Enum

map_view_width = 63
map_view_height = 63

map_width = map_view_width * 3
map_height = map_view_height *3
	
panel_width = 20
panel_height = map_view_height

screen_width = map_view_width + panel_width
screen_height = map_view_height

panel_x = screen_width - panel_width
panel_y = screen_height - panel_height	

bar_width = 15

message_x = 1
message_y = 5
message_width = 20
message_height = 40

colors = {
		'dark_wall': tcod.Color(0, 0, 100),
		'dark_ground': tcod.Color(50, 50, 150),
		'light_wall': tcod.darkest_blue,
		'light_ground': tcod.desaturated_blue
}

CAMERA_MOVE_BORDER = 20

class RenderOrder(Enum):
	PLAYER = 1
	ITEM = 2
	BUILDING = 3

class Characters(Enum):
	SMILEY = tcod.tileset.CHARMAP_CP437[1]
	FILLED_SMILEY = tcod.tileset.CHARMAP_CP437[2]
	HEART = tcod.tileset.CHARMAP_CP437[3]
	DIAMOND = tcod.tileset.CHARMAP_CP437[4]

	DOT = tcod.tileset.CHARMAP_CP437[7]
	RIGHT = tcod.tileset.CHARMAP_CP437[16]
	LEFT = tcod.tileset.CHARMAP_CP437[17]
	UP = tcod.tileset.CHARMAP_CP437[30]
	DOWN = tcod.tileset.CHARMAP_CP437 [31]

class Camera:
	def __init__(self, x: int, y: int, border: int = CAMERA_MOVE_BORDER):
		self.x = x
		self.y = y
		self.border = border
		self.zoomed_in_x = x
		self.zoomed_in_y = y


	def update(self, playerx, playery, zoomed_out):
		if playerx < self.x + self.border and self.x >= 0:
			self.x -= 1
		elif playerx > self.x + map_view_width - self.border and self.x <= map_width:
			self.x += 1
		elif playery < self.y + self.border and self.y >= 0:
			self.y -= 1
		elif playery > self.y + map_view_height - self.border and self.y <= map_height:
			self.y += 1
	
	def toggle_zoom(self, zoom_out):
		if zoom_out:
			self.zoomed_in_x = self.x
			self.zoomed_in_y = self.y
		else:
			self.x = self.zoomed_in_x
			self.y = self.zoomed_in_y

#TODO: Stop passing game_map object around, just take what you need
class Render:
	def __init__(self):
		self.zoom_factor = 1

	def render_bar(self, panel, x, y, total_width, name, value, maximum, bar_color, back_color):
		bar_width = int(float(value) / maximum * total_width)
		tcod.console_set_default_background(panel, back_color)
		tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)
		
		tcod.console_set_default_background(panel, bar_color)
		
		if bar_width > 0:
			tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)
			
		tcod.console_set_default_foreground(panel, tcod.white)
		tcod.console_print_ex(panel, int(x + total_width / 2), y, tcod.BKGND_NONE, tcod.CENTER, '{0}: {1}/{2}'.format(name, value, maximum))

	def render_all(self, con, panel, entities, game_map, message_log, camera):
		self.zoom_factor = 1
		if game_map.zoomed_out:
			self.zoom_factor = 3
		for y in range(map_view_height):
			for x in range(map_view_width):
				wall = game_map.tiles[camera.x + x][camera.y + y].block_sight	
				if wall:
					tcod.console_set_char_background(con, floor(x/self.zoom_factor), floor(y/self.zoom_factor), colors.get('light_wall'), tcod.BKGND_SET)
				else:
					tcod.console_set_char_background(con, floor(x/self.zoom_factor), floor(y/self.zoom_factor), colors.get('light_ground'), tcod.BKGND_SET)	
		for entity in entities:
			self.draw_entity(con, entity, camera, game_map.zoomed_out)
		
		tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
		
		#render HUD
		tcod.console_set_default_background(panel, tcod.black)
		tcod.console_clear(panel)
		#print messages one line at a time
		y = message_log.y
		for message in message_log.messages:
			tcod.console_set_default_foreground(panel, message.color)
			tcod.console_print_ex(panel, message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
			y +=1
			
		#replace tens with fuel variables
		self.render_bar(panel, 1, 1, bar_width, 'FUEL', 10, 10, tcod.light_red, tcod.dark_red)
		tcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, panel_x, panel_y)
		
	
	def clear_all(self, con, entities, camera, zoomed_out): #TODO: Something is wrong here if I have to pass zoomed_out. We need a better class structure
		for entity in entities:
			self.clear_entity(con, entity, camera, zoomed_out)
	

	def entity_coordinate(self, coord: int):
		return floor((coord - (coord%self.zoom_factor))/self.zoom_factor)


	def draw_entity(self, con, entity, camera, zoomed_out):
		tcod.console_set_default_foreground(con, entity.color)
		if zoomed_out:
			tcod.console_put_char(con, floor(entity.x/self.zoom_factor), floor(entity.y/self.zoom_factor), entity.char, tcod.BKGND_NONE)
		else:
			for coord in entity.coordinates:
				tcod.console_put_char(con, self.entity_coordinate((coord[0] - camera.x)), self.entity_coordinate(coord[1] - camera.y), entity.char, tcod.BKGND_NONE)

			
	def clear_entity(self, con, entity, camera, zoomed_out):
		if zoomed_out:
			tcod.console_put_char(con, floor(entity.x/self.zoom_factor), floor(entity.y/self.zoom_factor), ' ', tcod.BKGND_NONE)
		else:	
			for coord in entity.coordinates:
				tcod.console_put_char(con, self.entity_coordinate(coord[0] - camera.x), self.entity_coordinate(coord[1] - camera.y), " ", tcod.BKGND_NONE)



