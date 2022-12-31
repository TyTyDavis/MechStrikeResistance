import os

import tcod
from entities.mech import Mech
from input_handler import handle_keys
from game_messages import MessageLog, Message
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all
from entities.entity import Entity, get_blocking_entities_at_location


directory = os.path.dirname(__file__)
font_file = os.path.join(directory, 'static/cp437_16x16.png')


def main():
	map_width = 63
	map_height = 63
	
	panel_width = 20
	panel_height = map_height

	screen_width = map_width + panel_width
	screen_height = map_height

	panel_x = screen_width - panel_width
	panel_y = screen_height - panel_height
	
	

	bar_width = 15
	
	message_x = 1
	message_y = 5
	message_width = 20
	message_height = 40
	
	LIMIT_FPS = 20
	
	tcod.sys_set_fps(LIMIT_FPS)
	
	

	
	colors = {
		'dark_wall': tcod.Color(0, 0, 100),
		'dark_ground': tcod.Color(50, 50, 150),
		'light_wall': tcod.darkest_blue,
		'light_ground': tcod.desaturated_blue
	}
	player = Entity(0, 0, "@", tcod.white, 'Player', blocks=True)
	
	entities = [player]
	tcod.console_set_custom_font(font_file, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INROW)
	tcod.console_init_root(screen_width, screen_height, 'Mech Strike: Resistance', False)

	con = tcod.console_new(screen_width, screen_height)
	panel = tcod.console_new(panel_width, panel_height)
	game_map = GameMap(map_width, map_height)
	game_map.make_map(map_width, map_height, player, entities)
	
	#test stuff
	entities.insert(0, Mech(9,9, tcod.lighter_orange, 'Mech'))
	
	message_log = MessageLog(message_x, message_y, message_width, message_height)
	
	key = tcod.Key()
	mouse = tcod.Mouse()
	
	game_state = GameStates.PLAYERS_TURN
	
	while not tcod.console_is_window_closed():
	#game loop
		tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
	
			
		render_all(con, panel, entities, game_map, message_log, screen_width, screen_height, bar_width, panel_height, panel_x, panel_y, colors)
		
		
		tcod.console_flush()

		clear_all(con, entities)

		action = handle_keys(key)

		move = action.get('move')
		exit = action.get('exit')
		fullscreen = action.get('fullscreen')
		inventory = action.get('inventory')

		if move and game_state == GameStates.PLAYERS_TURN:
			dx, dy = move
			destination_x = player.x + dx
			destination_y = player.y + dy
			
			if not game_map.is_blocked(destination_x, destination_y):
				target = get_blocking_entities_at_location(entities, destination_x, destination_y)

				if isinstance(target, Mech) or not target:
					player.move(dx, dy)
					fov_recompute = True
				else:
					pass
				
		
		if inventory:
			message_log.add_message(Message('Inventory is empty', tcod.white))
			print(message_log.messages[0].text)
		if exit:
			return True

		if fullscreen:
			tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
			

if __name__ == '__main__':
	main()
		
	
