import tcod

from components import components
from render_functions import Characters

simple_mech_design = [
    (Characters.UP_POINTING_TRIANGLE_POINTING_TRIANGLE.value,tcod.lighter_orange), (Characters.UP_POINTING_TRIANGLE_POINTING_TRIANGLE.value,tcod.lighter_orange), (Characters.UP_POINTING_TRIANGLE_POINTING_TRIANGLE.value,tcod.lighter_orange),
    (Characters.UP_POINTING_TRIANGLE_POINTING_TRIANGLE.value,tcod.lighter_orange), (Characters.UP_POINTING_TRIANGLE_POINTING_TRIANGLE.value,tcod.lighter_orange), (Characters.UP_POINTING_TRIANGLE_POINTING_TRIANGLE.value,tcod.lighter_orange),
    (Characters.UP_POINTING_TRIANGLE_POINTING_TRIANGLE.value,tcod.lighter_orange), (Characters.UP_POINTING_TRIANGLE_POINTING_TRIANGLE.value,tcod.lighter_orange), (Characters.UP_POINTING_TRIANGLE_POINTING_TRIANGLE.value,tcod.lighter_orange),
]

def player(x, y):
    return (
        components.Player(),
        components.PlayerTurn(),
        components.Coordinates([(x,y)]),
        components.Collision(),
        components.Description(name='player'),
        components.Render([("@", tcod.white)]),
        components.RenderZoomedOut(("@", tcod.white)), #TODO: for debugging
        components.Moves(),
        components.Velocity(),
    )

def mech(x, y):
    return(
        components.EnemyTurn(),
        components.Coordinates([
            (x, y), (x+1, y), (x+2, y),
            (x, y+1), (x+1, y+1), (x+2, y+1),
            (x, y+2), (x+1, y+2), (x+2, y+2),
        ]),
        components.Render(simple_mech_design),
        components.RenderZoomedOut((Characters.UP_POINTING_TRIANGLE_POINTING_TRIANGLE.value,tcod.lighter_orange)),
        components.Description(name='test mech'),
        components.Moves(),
        components.Velocity(),

    )