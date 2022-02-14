from enum import Enum, auto


class ClefType(Enum):

    """Types of clefs.

    The enumeration values are not meaningful.
    """

    treble = auto()
    """A typical treble clef."""

    bass = auto()
    """A bass clef."""

    bass_8vb = auto()
    """An octave-down transposing bass clef."""

    tenor = auto()
    """A tenor clef."""

    alto = auto()
    """An alto clef."""
