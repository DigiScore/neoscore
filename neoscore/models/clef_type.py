from enum import Enum, auto


class ClefType(Enum):

    """Types of clefs.

    The enumeration values are not meaningful.
    """

    TREBLE = auto()
    """A typical treble clef."""

    BASS = auto()
    """A bass clef."""

    BASS_8VB = auto()
    """An octave-down transposing bass clef."""

    TENOR = auto()
    """A tenor clef."""

    ALTO = auto()
    """An alto clef."""

    # TODO HIGH support treble 8vb and other C-clefs
