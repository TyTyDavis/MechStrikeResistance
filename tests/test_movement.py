import tcod
import pytest

from components import components
from entities import entities
from processors import processors, player_processor
from visuals.characters import Characters


@pytest.fixture
def needed_processors(world):
    processor_list = [
        player_processor.PlayerProcessor(),
	    processors.MovementProcessor(), 
	    processors.MechProcessor(),
    ]
    for processor in processor_list:
        world.add_processor(processor)

def test_mech_move_by_player(world, needed_processors, player):
    mech = world.create_entity()
    for component in entities.mech(27, 27):
        world.add_component(mech, component)

    world.add_component(mech, components.Controlled())
    world.remove_component(player, components.Controlled)
    player_component = world.component_for_entity(player, components.Player)
    player_component.vehicle = mech

    coordinates = world.component_for_entity(mech, components.Coordinates)
    assert coordinates.coordinates == [
        (27, 27), 
        (28, 27), 
        (29, 27), 
        (27, 28), 
        (28, 28), 
        (29, 28), 
        (27, 29), 
        (28, 29), 
        (29, 29)
    ]

    world.action = {"move": (0, -1)}

    world.process()

    coordinates = world.component_for_entity(mech, components.Coordinates)
    assert coordinates.coordinates == [
        (27, 24), 
        (28, 24), 
        (29, 24), 
        (27, 25), 
        (28, 25), 
        (29, 25), 
        (27, 26), 
        (28, 26), 
        (29, 26)
    ]
    player_coordinates = world.component_for_entity(player, components.Coordinates)
    assert player_coordinates.coordinates[0] == coordinates.coordinates[4]

    world.action = {"move": (0, 1)}

    world.process()

    coordinates = world.component_for_entity(mech, components.Coordinates)
    assert coordinates.coordinates == [
        (27, 27), 
        (28, 27), 
        (29, 27), 
        (27, 28), 
        (28, 28), 
        (29, 28), 
        (27, 29), 
        (28, 29), 
        (29, 29)
    ]
    player_coordinates = world.component_for_entity(player, components.Coordinates)
    assert player_coordinates.coordinates[0] == coordinates.coordinates[4]

    world.action = {"move": (1, 0)}

    world.process()

    coordinates = world.component_for_entity(mech, components.Coordinates)
    assert coordinates.coordinates == [
        (30, 27), 
        (31, 27), 
        (32, 27), 
        (30, 28), 
        (31, 28), 
        (32, 28), 
        (30, 29), 
        (31, 29), 
        (32, 29)
    ]
    player_coordinates = world.component_for_entity(player, components.Coordinates)
    assert player_coordinates.coordinates[0] == coordinates.coordinates[4]

    world.action = {"move": (-1, 0)}

    world.process()

    coordinates = world.component_for_entity(mech, components.Coordinates)
    assert coordinates.coordinates == [
        (27, 27), 
        (28, 27), 
        (29, 27), 
        (27, 28), 
        (28, 28), 
        (29, 28), 
        (27, 29), 
        (28, 29), 
        (29, 29)
    ]
    player_coordinates = world.component_for_entity(player, components.Coordinates)
    assert player_coordinates.coordinates[0] == coordinates.coordinates[4]


def test_mech_rotation(world, needed_processors, player):
    mech = world.create_entity()
    for component in entities.mech(27, 27):
        world.add_component(mech, component)

    world.add_component(mech, components.Controlled())
    world.remove_component(player, components.Controlled)

    render = world.component_for_entity(mech, components.Render)
    mech_component = world.component_for_entity(mech, components.Mech)

    assert mech_component.facing == components.Directions.SOUTH.value
    assert render.chars == entities.simple_mech_design

    world.action = {"face": components.Directions.EAST.value}
    world.process()
    render = world.component_for_entity(mech, components.Render)

    assert render.chars == [
        (Characters.DIAMOND.value,tcod.blue), (Characters.UP_POINTING_TRIANGLE.value,tcod.blue), (Characters.UPPER_HALF_BLOCK.value,tcod.white),
        (Characters.RIGHT_HALF_BLOCK.value,tcod.blue), (Characters.RIGHT_POINTING_TRIANGLE.value,tcod.red), (Characters.LEFT_HALF_BLOCK.value,tcod.white),
        (Characters.DIAMOND.value,tcod.blue), (Characters.DOWN_POINTING_TRIANGLE.value,tcod.blue), (Characters.LOWER_HALF_BLOCK.value,tcod.white),
    ]

    world.action = {"face": components.Directions.WEST.value}
    world.process()
    render = world.component_for_entity(mech, components.Render)

    assert render.chars == [
        (Characters.UPPER_HALF_BLOCK.value,tcod.white), (Characters.UP_POINTING_TRIANGLE.value,tcod.blue), (Characters.DIAMOND.value,tcod.blue),
        (Characters.RIGHT_HALF_BLOCK.value,tcod.white), (Characters.LEFT_POINTING_TRIANGLE.value,tcod.red), (Characters.LEFT_HALF_BLOCK.value,tcod.blue),
        (Characters.LOWER_HALF_BLOCK.value,tcod.white), (Characters.DOWN_POINTING_TRIANGLE.value,tcod.blue), (Characters.DIAMOND.value,tcod.blue),
    ]

