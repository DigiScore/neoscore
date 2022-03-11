from enum import Enum
from typing import Union


class AccidentalType(Enum):

    """A logical accidental descriptor.

    These are used both in `Pitch` manipulations and in
    graphical `Accidental` objects.

    The numeric values of each enum refer to the pitch class offset
    associated with the accidental.
    """

    FLAT = -1
    """A flat accidental"""

    NATURAL = 0
    """A natural accidental"""

    SHARP = 1
    """A sharp accidental"""

    F = FLAT
    """Shorthand for `AccidentalType.flat`"""

    N = NATURAL
    """Shorthand for `AccidentalType.natural`"""

    S = SHARP
    """Shorthand for `AccidentalType.sharp`"""
