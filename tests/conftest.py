import pytest
import tcod

from entities import entities
from processors import add_processors
from world import World

console = tcod.Console(63, 63, order="F")
panel = tcod.Console(20, 63, order="F")

@pytest.fixture
def world():
    world = World(console, panel)

    return world


@pytest.fixture
def all_processors(world):
    add_processors(world)


@pytest.fixture
def player(world):
    player = world.create_entity()
    for component in entities.player(20,20):
        world.add_component(player, component)
    
    return player
