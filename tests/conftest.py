import pytest

from world import World

console = tcod.Console(63, 63, order="F")
panel = tcod.Console(20, 63, order="F")

@pytest.fixture
def world():
    world = World(console, panel)