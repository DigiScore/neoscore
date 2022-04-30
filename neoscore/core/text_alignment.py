from enum import Enum, auto


class AlignmentX(Enum):
    """Enum defining horizontal text alignments."""

    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


class AlignmentY(Enum):
    """Enum defining vertical text alignments.

    Only baseline and center alignments are currently supported.
    """

    BASELINE = auto()
    CENTER = auto()
