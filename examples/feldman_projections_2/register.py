from enum import Enum

from examples.feldman_projections_2.grid_unit import GridUnit


class Register(Enum):

    HIGH = GridUnit(0)
    MEDIUM = GridUnit(1)
    LOW = GridUnit(2)

    H = HIGH
    M = MEDIUM
    L = LOW
