import tcod

from enum import Enum

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


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
	bar_width = int(float(value) / maximum * total_width)
	tcod.console_set_default_background(panel, back_color)
	tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)

	tcod.console_set_default_background(panel, bar_color)

	if bar_width > 0:
		tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

	tcod.console_set_default_foreground(panel, tcod.white)
	tcod.console_print_ex(panel, int(x + total_width / 2), y, tcod.BKGND_NONE, tcod.CENTER, '{0}: {1}/{2}'.format(name, value, maximum))

def render_all(con, panel, entities, game_map, message_log, screen_width, screen_height, bar_width, panel_height, panel_x, panel_y, colors):
	for y in range(game_map.height):
		for x in range(game_map.width):
			wall = game_map.tiles[x][y].block_sight
			if wall:
				tcod.console_set_char_background(con, x, y, colors.get('light_wall'), tcod.BKGND_SET)
			else:
				tcod.console_set_char_background(con, x, y, colors.get('light_ground'), tcod.BKGND_SET)

	for entity in entities:
		draw_entity(con, entity)

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
	render_bar(panel, 1, 1, bar_width, 'FUEL', 10, 10, tcod.light_red, tcod.dark_red)
	tcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, panel_x, panel_y)


def clear_all(con, entities):
	for entity in entities:
		clear_entity(con, entity)

def draw_entity(con, entity):
	tcod.console_set_default_foreground(con, entity.color)

	for x in range(entity.x, entity.x+entity.size):
		for y in range(entity.y, entity.y+entity.size):
			tcod.console_put_char(con, x, y, entity.char, tcod.BKGND_NONE)


def clear_entity(con, entity):
	tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
