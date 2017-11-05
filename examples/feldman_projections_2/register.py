from enum import Enum, auto


class Register(Enum):

    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

    H = HIGH
    M = MEDIUM
    L = LOW
