from enum import Enum


class VirtualAccidental(Enum):

    """A logical accidental descriptor.

    These are used both in `Pitch` manipulations and in
    graphical `Accidental` objects.

    The numeric values of each enum refer to the pitch class offset
    associated with the accidental.
    """

    flat = -1
    """A flat accidental"""

    natural = 0
    """A natural accidental"""

    sharp = 1
    """A sharp accidental"""

    f = flat
    """Shorthand for `VirtualAccidental.flat`"""

    n = natural
    """Shorthand for `VirtualAccidental.natural`"""

    s = sharp
    """Shorthand for `VirtualAccidental.sharp`"""
