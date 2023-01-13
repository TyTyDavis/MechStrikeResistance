from dataclasses import dataclass as component
from enum import Enum
from typing import List


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

class Directions(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    
@component
class Facing:
    direction: Directions

@component
class Collision:
    pass

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

