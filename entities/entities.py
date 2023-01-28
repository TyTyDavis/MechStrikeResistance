import tcod

from components import components
from visuals.characters import Characters

simple_mech_design = [
    (Characters.DIAMOND.value,tcod.blue), (Characters.LOWER_HALF_BLOCK.value,tcod.blue), (Characters.DIAMOND.value,tcod.blue),
    (Characters.LEFT_POINTING_TRIANGLE.value,tcod.blue), (Characters.DOWN_POINTING_TRIANGLE.value,tcod.red), (Characters.RIGHT_POINTING_TRIANGLE.value,tcod.blue),
    (Characters.LEFT_HALF_BLOCK.value,tcod.white), (Characters.UPPER_HALF_BLOCK.value,tcod.white), (Characters.RIGHT_HALF_BLOCK.value,tcod.white),
]

def player(x, y):
    return (
        components.Player(),
        components.PlayerTurn(),
        components.Coordinates([(x,y)]),
        components.Collision(),
        components.Description(name='player'),
        components.Render([("@", tcod.white)]),
        components.Moves(),
        components.Velocity(),
        components.Size(1),
        components.Inventory(money=100),
        components.HitPoints(hp=50, maxHP=50),
    )

def mech(x, y):
    return(
        components.Mech(facing=components.Directions.SOUTH.value),
        components.EnemyTurn(),
        components.Coordinates([
            (x, y), (x+1, y), (x+2, y),
            (x, y+1), (x+1, y+1), (x+2, y+1),
            (x, y+2), (x+1, y+2), (x+2, y+2),
        ]),
        components.Render(simple_mech_design),
        components.RenderZoomedOut((Characters.DOWN_POINTING_TRIANGLE.value,tcod.red)),
        components.Description(name='test mech'),
        components.Moves(),
        components.Velocity(),
        components.Size(3),
        components.Inventory(),
        components.HitPoints(hp=300, maxHP=300),

    )