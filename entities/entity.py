from typing import List
import tcod
import math


class Entity:
	def __init__(self, x: int, y: int, char: str, color, name: str, size: int =1, blocks: bool = False):
		self.x: int = x
		self.y: int = y
		self.char: str = char
		self.color = color
		self.name: str = name
		self.blocks: bool = blocks
		self.size: int = size
		self.coordinates: List = []
		
		self.update_coordinates()


	def update_coordinates(self):
		if self.size == 1:
			self.coordinates = [(self.x, self.y)]
		else:
			self.coordinates = []
			for x in range(self.x, self.x+self.size):
				for y in range(self.y, self.y+self.size):
					self.coordinates.append((x,y))

	def place(self, x, y):
		self.x, self.y = x, y
		self.update_coordinates()
	

	def move(self, dx, dy):
		#move by a given amount
		self.x += dx
		self.y += dy
		self.update_coordinates()
	

	def move_towards(self, target_x, target_y, game_map, entities):
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx **2 + dy **2) + 1
		dx = int(round(dx / distance))
		dy = int(round(dy / distance))

		if not (game_map.is_blocked(self. x + dx, self.y + dy) or get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
			self.move(dx, dy)
	

	def move_astar(self, target, entities, game_map):
		fov = tcod.map_new(game_map.width, game_map.height)

		for y1 in range(game_map.height):
			for x1 in range(game_map.width):
				tcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight, not game_map.tiles[x1][y1].blocked)

			for entity in entities:
				if entity.blocks and entity != self and entity != target:
					tcod.map_set_properties(fov, entity.x, entity.y, True, False)

			#Allocate A* path
			#the 1.41 is the normal diagonal cost of moving. 0.0 if no diagonal movement
			my_path = tcod.path_new_using_map(fov, 1.41)

			tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

			if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
				x, y = tcod.path_walk(my_path, True)
				if x or y:
					self.x = x
					self.y = y
			else:
				self.move_towards(target.x, target.y, game_map, entities)

			tcod.path_delete(my_path)
	
	
	def distance_to(self, other):
		dx = other.x - self.x
		dy = other.y - self.y
		return math.sqrt(dx ** 2 + dy ** 2)
	

def get_blocking_entities_at_location(entities, destination_x, destination_y):
	for entity in entities:
		if (destination_x, destination_y) in entity.coordinates:
			return entity
	return None
