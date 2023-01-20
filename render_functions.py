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

CAMERA_MOVE_BORDER = 10

class RenderOrder(Enum):
	PLAYER = 1
	ITEM = 2
	BUILDING = 3

class Characters(Enum):
	SMILEY = chr(0x263A)
	FILLED_SMILEY = chr(0x263B)
	HEART = chr(0x2665)
	DIAMOND = chr(0x2666)

	BULLET = chr(0x2022)

	RIGHT_POINTING_TRIANGLE = chr(0x25BA)
	LEFT_POINTING_TRIANGLE =chr(0x25C4)
	UP_POINTING_TRIANGLE = chr(0x25B2)
	DOWN_POINTING_TRIANGLE = chr(0x25BC)

	LOWER_HALF_BLOCK = chr(0x2584)
	LEFT_HALF_BLOCK = chr(0x258C)
	RIGHT_HALF_BLOCK = chr(0x2590)
	UPPER_HALF_BLOCK = chr(0x2580)
	RECTANGLE = chr(0x25AC)


	LIGHT_SHADE = chr(0x2591)
	MEDIUM_SHADE = chr(0x2592)

class Camera:
	def __init__(self, x: int, y: int, border: int = CAMERA_MOVE_BORDER):
		self.x = x
		self.y = y
		self.border = border
		self.zoomed_in_x = x
		self.zoomed_in_y = y


	def update(self, playerx, playery, zoomed_out):
		if playerx < self.x + self.border and self.x > 0:
			self.x -= 1
		elif playerx > self.x + map_view_width - self.border and self.x + map_view_width < map_width:
			self.x += 1
		elif playery < self.y + self.border and self.y > 0:
			self.y -= 1
		elif playery > self.y + map_view_height - self.border and self.y + map_view_height < map_height:
			self.y += 1
	
	def toggle_zoom(self, zoom_out):
		if zoom_out:
			self.zoomed_in_x = self.x
			self.zoomed_in_y = self.y
		else:
		#TODO This should recenter the camera on the players new position
			self.x = self.zoomed_in_x
			self.y = self.zoomed_in_y