from enum import Enum

from examples.feldman_projection_2.grid_unit import GridUnit


class Register(Enum):

    """The pitch register of an event.

    The enum values encode the corresponding Y coordinates in GridUnits.
    """

    HIGH = GridUnit(0)
    MEDIUM = GridUnit(1)
    LOW = GridUnit(2)

    H = HIGH
    M = MEDIUM
    L = LOW
