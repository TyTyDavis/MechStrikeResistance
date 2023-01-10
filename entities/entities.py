import tcod

from components import components
from render_functions import Characters

simple_mech_design = [
    (Characters.UP.value,tcod.lighter_orange), (Characters.UP.value,tcod.lighter_orange), (Characters.UP.value,tcod.lighter_orange),
    (Characters.UP.value,tcod.lighter_orange), (Characters.UP.value,tcod.lighter_orange), (Characters.UP.value,tcod.lighter_orange),
    (Characters.UP.value,tcod.lighter_orange), (Characters.UP.value,tcod.lighter_orange), (Characters.UP.value,tcod.lighter_orange),
]

def player(x, y):
    return (
        components.Player(),
        components.PlayerTurn(),
        components.Coordinates([(x,y)]),
        components.RenderZoomedIn('@'),
        components.Collision(),
        components.Description(name='player'),
        components.RenderZoomedIn(["@", tcod.white]),
        components.Moves(),
        components.Velocity(),
    )

def mech(x, y):
    return(
        components.EnemyTurn(),
        components.Coordinates([(x, y)]),
        components.RenderZoomedIn(simple_mech_design),
        components.RenderZoomedIn((Characters.UP.value,tcod.lighter_orange)),
        components.Description(name='test mech'),
        components.Moves(),
        components.Velocity(),

    )