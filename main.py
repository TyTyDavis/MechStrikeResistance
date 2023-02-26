import os

import tcod
from input_handler import handle_keys
from game_messages import MessageLog, Message
from game_states import GameStates
from map.game_map import GameMap
from render_functions import (
	map_view_width,
	panel_width,
	screen_height, 
	screen_width, 
)
from components import components
from entities.entity import Entity, get_blocking_entities_at_location
from entities import entities
from processors import processors, render_processors, input_processors, player_processor
from world import World


directory = os.path.dirname(__file__)
font_file = os.path.join(directory, 'static/cp437_16x16.png')

PROCESSORS_LIST = [
	input_processors.InputProcessor(),
	player_processor.PlayerProcessor(),
	processors.MovementProcessor(), 
	processors.MechProcessor(),
	render_processors.CameraProcessor(), 
	render_processors.HUDProcessor(),
]

def main(): 
	
	tileset = tcod.tileset.load_tilesheet(
        font_file, 16,16, tcod.tileset.CHARMAP_CP437,
    )
	with tcod.context.new(
			columns=screen_width, rows=screen_height, tileset=tileset, title="Mech Strike: Resistance"
		) as context:
		console = tcod.Console(map_view_width, screen_height, order="F")
		panel = tcod.Console(panel_width, screen_height, order="F")

		master_console = tcod.Console(83, 63, order="F")

		world = World(console, panel)
		
		mech = world.create_entity()
		for component in entities.mech(27, 27):
			world.add_component(mech, component)

		player = world.create_entity()
		for component in entities.player(20,20):
			world.add_component(player, component)

		test_mech = world.create_entity()
		for component in entities.mech(27, 42):
			world.add_component(test_mech, component)
		

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
			

			#console.print(x=2, y=2, string="player: " + str(player_position))
			#console.print(x=2, y=3, string="camera: " + str((world.camera.x, world.camera.y)))
			console.blit(master_console, 0, 0, 0, 0, 63, 63)
			panel.blit(master_console, 63, 0, 0, 0)
			context.present(master_console, keep_aspect=True, align=[0.0,0.0])
			

			

			for event in tcod.event.wait():
				if isinstance(event, tcod.event.Quit):
					raise SystemExit(0)





if __name__ == '__main__':
	main()
