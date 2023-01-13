import os

import tcod
from input_handler import handle_keys
from game_messages import MessageLog, Message
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import (
	screen_height, 
	screen_width, 
)
from components import components
from entities.entity import Entity, get_blocking_entities_at_location
from entities import entities
from processors import processors, render_processors, input_processors
from world import World


directory = os.path.dirname(__file__)
font_file = os.path.join(directory, 'static/cp437_16x16.png')

colors = {
		'dark_wall': tcod.Color(0, 0, 100),
		'dark_ground': tcod.Color(50, 50, 150),
		'light_wall': tcod.darkest_blue,
		'light_ground': tcod.desaturated_blue
	}

message_x = 1
message_y = 5
message_width = 20
message_height = 40

LIMIT_FPS = 20

PROCESSORS_LIST = [
	input_processors.InputProcessor(),
	processors.PlayerProcessor(),
	processors.MovementProcessor(), 
	render_processors.CameraProcessor(), 
]
def main(): 
	tcod.sys_set_fps(LIMIT_FPS)

	tcod.console_set_custom_font(font_file, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INROW)
	tcod.console_init_root(screen_width, screen_height, 'Mech Strike: Resistance', False)

	#con = tcod.console_new(screen_width, screen_height)
	#panel = tcod.console_new(panel_width, panel_height)
	#TODO: Fix this, no hardcoding
	con = tcod.console.Console(63+20, 63)
	panel = tcod.console.Console(20, 63)

	key = tcod.Key()
	mouse = tcod.Mouse()

	world = World(con, panel)
	
	mech = world.create_entity()
	for component in entities.mech(63 + 8, 63 + 8):
		world.add_component(mech, component)

	player = world.create_entity()
	for component in entities.player(93, 94):
		world.add_component(player, component)
	

	world.add_processor(render_processors.ClearProcessor(), 0)
	for processor in PROCESSORS_LIST:
		world.add_processor(processor)
	world.add_processor(render_processors.MapRenderProcessor(),1)
	world.add_processor(render_processors.EntityRenderProcessor(), 100)

	while not tcod.console_is_window_closed():
	#game loop
		tcod.console_flush()
		player_position = world.player_coordinates()
		tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

		world.process()





if __name__ == '__main__':
	main()
