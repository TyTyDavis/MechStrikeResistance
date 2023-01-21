import os

import tcod
from input_handler import handle_keys
from game_messages import MessageLog, Message
from game_states import GameStates
from map.game_map import GameMap
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


PROCESSORS_LIST = [
	input_processors.InputProcessor(),
	processors.PlayerProcessor(),
	processors.MovementProcessor(), 
	processors.MechProcessor(),
	render_processors.CameraProcessor(), 
]
def main(): 
	
	tileset = tcod.tileset.load_tilesheet(
        font_file, 16,16, tcod.tileset.CHARMAP_CP437,
    )
	with tcod.context.new(  # New window for a console of size columns×rows.
			columns=screen_width, rows=screen_height, tileset=tileset, title="Mech Strike: Resistance"
		) as context:
		#con = tcod.console_new(screen_width, screen_height)
		#panel = tcod.console_new(panel_width, panel_height)
		#TODO: Fix this, no hardcoding
		console = tcod.Console(63, 63, order="F")
		panel = tcod.Console(20, 63, order="F")

		world = World(console, panel)
		
		mech = world.create_entity()
		for component in entities.mech(30, 30):
			world.add_component(mech, component)

		player = world.create_entity()
		for component in entities.player(20,20):
			world.add_component(player, component)
		

		world.add_processor(render_processors.ClearProcessor(), 100)
		for processor in PROCESSORS_LIST:
			world.add_processor(processor)
		world.add_processor(render_processors.MapRenderProcessor(),2)
		world.add_processor(render_processors.EntityRenderProcessor(), 2)
		world.add_processor(processors.MechProcessor(),1)
		
		while True:
		#game loop
			console.clear()
			world.process()
			
			player_position = world.player_coordinates()
			
			console.print(x=2, y=2, string="player: " + str(player_position))
			console.print(x=2, y=3, string="camera: " + str((world.camera.x, world.camera.y)))
			
			context.present(console)

			

			for event in tcod.event.wait():
				if isinstance(event, tcod.event.Quit):
					raise SystemExit(0)





if __name__ == '__main__':
	main()
