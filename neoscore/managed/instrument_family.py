from enum import Enum, auto


class InstrumentFamily(Enum):

    """Common instrument categories."""

    STRING = auto()
    """String instruments"""

    WIND = auto()
    """Woodwind instruments"""

    BRASS = auto()
    """Brass instruments"""

    PERCUSSION = auto()
    """Percussion instruments"""

    KEYBOARD = auto()
    """Keyboard instruments"""

    ELECTRONIC = auto()
    """Primarily electronic instruments"""

    VOICE = auto()
    """Singing or speaking instruments"""

    OTHER = auto()
    """Catch-all for everything else"""
