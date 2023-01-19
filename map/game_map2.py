import tcod
from entities.entity import Entity
from map.tile import Tile
from map.rectangle import Rect
from random import randint
from statistics import mode


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

class GameMap:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.tiles = self.initialize_tiles()
		self.zoom_tiles = []
		self.zoomed_out = False
		
	def initialize_tiles(self):
		tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]
		
		
		return tiles
	
	def make_map(self, map_width, map_height):
		rooms = []
		num_rooms = 0
		x = 0
		y = 0
		w = int(map_width - 1)
		h = int(map_height - 1)
			
		new_room = Rect(x, y, w, h)
		self.create_room(new_room)

					
			
		rooms.append(new_room)
		num_rooms += 1
						
			
		
	def create_room(self, room):
		for x in range(room.x1 + 1, room.x2):
			for y in range(room.y1 + 1, room.y2):
				self.tiles[x][y].blocked = True
				self.tiles[x][y].block_sight = False
				
	def create_h_tunnel(self, x1, x2, y):
		for x in range(min(x1, x2), max(x1, x2) + 1):
			self.tiles[x][y].blocked = False
			self.tiles[x][y].block_sight = False
			
	def create_v_tunnel(self, y1, y2, x):
		for y in range(min(y1, y2), max(y1, y2) + 1):
			self.tiles[x][y].blocked = False
			self.tiles[x][y].block_sight = False
			
	def place_entities(self, room, entities, max_monsters_per_room):
		number_of_monsters = randint (0, max_monsters_per_room)
		
		for i in range(number_of_monsters):
			x = randint(room.x1 + 1, room.x2 - 1)
			y = randint(room.y1 + 1, room.y2 - 1)
			
			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				if randint (0, 100) < 80:
					fighter_component = Fighter(hp=10, defense=0, power=3)
					ai_component = BasicMonster()
					
					monster = Entity(x, y, 'o', tcod.desaturated_green, 'Orc', blocks=True, fighter=fighter_component, ai=ai_component)
				else:
					fighter_component = Fighter(hp=16, defense=1, power=4)
					ai_component = BasicMonster()
					monster = Entity(x, y, 'T', tcod.darker_green, 'Troll', blocks=True, fighter=fighter_component, ai=ai_component)
				
				entities.append(monster)
				
	def is_blocked(self, x, y):
		if self.tiles[x][y].blocked:
			return True
		
		return False

	def zoom_tile(self, x, y):
		tiles = []
		for xx in range(x, x+3):
			for yy in range(y, y+3):
				tiles.append(self.tiles[xx][yy])
		
		return mode(tiles)

	def zoom_map(self):
		if self.zoomed_out:
			self.zoomed_out == False
		else:
			for x in range(0, map_width, 3):
				for y in range(0, map_height, 3):
					tile = self.zoom_tile(x, y)
					self.zoom_tiles[x][y] = tile

	def toggle_zoom(self):
		if self.zoomed_out:
			self.zoomed_out = False
		else:
			self.zoomed_out = True

