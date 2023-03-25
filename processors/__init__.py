from processors import handlers, input_processors, player_processor, processors, render_processors

PROCESSORS_LIST = [
	input_processors.InputProcessor(),
	player_processor.PlayerProcessor(),
	processors.AttackProcessor(),
	processors.MovementProcessor(), 
	render_processors.CameraProcessor(), 
	render_processors.HUDProcessor(),
]


def add_processors(world):
    world.add_processor(render_processors.ClearProcessor(), 100)
    for processor in PROCESSORS_LIST:
        world.add_processor(processor)
    world.add_processor(render_processors.MapRenderProcessor(),3)
    world.add_processor(render_processors.EntityRenderProcessor(), 3)
    world.add_processor(processors.MechProcessor(),2)
    world.add_processor(handlers.EventHandler(), 1)