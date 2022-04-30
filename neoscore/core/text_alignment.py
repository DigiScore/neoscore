from enum import Enum, auto


class HorizontalAlignment(Enum):
    """Enum defining horizontal text alignments."""

    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


class VerticalAlignment(Enum):
    """Enum defining vertical text alignments.

    Only baseline and center alignments are currently supported.
    """

    BASELINE = auto()
    CENTER = auto()
