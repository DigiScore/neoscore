from enum import Enum


class ClefType(Enum):

    """Types of clefs.

    The enumeration values are not meaningful.
    """

    treble = 0
    """A typical treble clef."""

    bass = 1
    """A bass clef."""

    bass_8vb = 2
    """An octave-down transposing bass clef."""

    tenor = 3
    """A tenor clef."""

    alto = 4
    """An alto clef."""
