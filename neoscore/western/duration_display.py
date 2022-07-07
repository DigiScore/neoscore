from __future__ import annotations

import math
from dataclasses import dataclass

from typing_extensions import TypeAlias

from neoscore.core.math_helpers import is_power_of_2

BaseDuration: TypeAlias = int
"""A base duration used to set notehead and rest glyphs.

Must be 0 or a power of 2. The values correspond to durations like so:

* 0: Double whole note
* 1: Whole note
* 2: Half note
* 4: Quarter note (etc)
"""


@dataclass(frozen=True)
class DurationDisplay:

    """The basic information about a :obj:`.Duration` needed to write a note with."""

    base_duration: BaseDuration

    dot_count: int

    def __post_init__(self):
        if not (is_power_of_2(self.base_duration) or self.base_duration == 0):
            raise ValueError("base_duration must be 0 or a power of 2")

    @property
    def flag_count(self) -> int:
        """Flag and beam count needed if used in a note"""
        if self.base_duration <= 4:
            return 0
        return int(math.log2(self.base_duration) - 2)

    @property
    def requires_stem(self) -> bool:
        return self.base_duration > 1
