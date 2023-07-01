from dataclasses import dataclass as component
from dataclasses import field
from enum import Enum
from typing import Any, List


@component
class Player:
    interactables: List[int] = field(default_factory=list)
    vehicle: int | None = None #entity id
    speed: int = 1


@component
class Controlled:
    pass


@component
class PlayerTurn:
    pass


@component
class EnemyTurn:
    pass


@component
class Inventory:
    items: list = field(default_factory=list) 
    money: int = 0
    capacity: int = 10

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
    name: str | None = None
    model_name: str = "Mech"
    embarked: bool = False #is the player in it?
    occupied: bool = False #is the player OR anyone else in it?
    

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
    speed: int = 1

@component
class Velocity:
    x: int = 0
    y: int = 0

@component
class Description:
    name: str = ""
    description: str = ""

@component
class Attack:
    melee_damage: int = 1


@component
class Item:
    pass

