from dataclasses import dataclass

from neoscore.models.interval import Interval


@dataclass(frozen=True)
class Transposition:

    """A pitch transposition represented as an interval"""

    interval: Interval
