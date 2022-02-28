from dataclasses import dataclass

from brown.models.interval import Interval


@dataclass(frozen=True)
class Transposition:

    """A pitch transposition represented as an interval"""

    interval: Interval
