from fractions import Fraction
from typing import Optional

from neoscore.models.beat_display import BeatDisplay


class Duration:
    def __init__(self):
        raise NotImplementedError

    @property
    def whole_note_fraction(self) -> Fraction:
        """The portion of a whole note occupied by this duration."""
        raise NotImplementedError

    @property
    def display(self) -> Optional[BeatDisplay]:
        """Determine how this duration should be logically displayed.


        If the duration cannot be represented without a tie (for
        instance a duration spanning 5 eighth notes), this returns
        `None` since tie structures cannot be unambiguously derived.
        """
        raise NotImplementedError
