from enum import Enum, auto


class InstrumentFamily(Enum):

    """Common instrument categories."""

    string = auto()
    """String instruments"""

    wind = auto()
    """Woodwind instruments"""

    brass = auto()
    """Brass instruments"""

    percussion = auto()
    """Percussion instruments"""

    keyboard = auto()
    """Keyboard instruments"""

    electronic = auto()
    """Primarily electronic instruments"""

    voice = auto()
    """Singing or speaking instruments"""

    other = auto()
    """Catch-all for everything else"""
