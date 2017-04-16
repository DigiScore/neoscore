from enum import Enum


class InstrumentFamily(Enum):

    """Common instrument categories."""

    string = 0
    """String instruments"""

    wind = 1
    """Woodwind instruments"""

    brass = 2
    """Brass instruments"""

    percussion = 3
    """Percussion instruments"""

    keyboard = 4
    """Keyboard instruments"""

    electronic = 5
    """Primarily electronic instruments"""

    voice = 6
    """Singing or speaking instruments"""

    other = 7
    """Catch-all for everything else"""
