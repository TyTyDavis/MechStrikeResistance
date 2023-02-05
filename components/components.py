from dataclasses import dataclass as component
from enum import Enum
from typing import Any, List


@component
class Player:
    pass


@component
class PlayerTurn:
    pass


@component
class EnemyTurn:
    pass


@component
class Inventory:
    money: int = 0

@component
class HitPoints:
    hp: int = 1
    maxHP: int = 50

class Directions(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"

@component
class Mech:
    facing: str = Directions.SOUTH.value

@component
class Coordinates:
    coordinates: List[tuple]


@component
class Size:
    size: int = 1


@component
class Render:
    chars: List[tuple]

@component
class RenderZoomedOut:
    char: tuple

@component
class Collision:
    with_mech: bool = True

@component
class Moves:
    pass

@component
class Velocity:
    x: int = 0
    y: int = 0

@component
class Embark:
    embarked: bool = False #is the player in it?
    occupied: bool = False #is the player OR anyone else in it?

@component
class Description:
    name: str = ""
    description: str = ""

