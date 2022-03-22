import math
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseDuration:
    """The duration value to use in determining a notehead or rest glyph type

    Given values must be 0 or a power of 2. The values correspond to glyphs in
    the following manner:

    * 0: double whole note/rest
    * 1: whole note/rest
    * 2: half note/rest
    * 4: quarter note/rest
    * 8: eighth note/rest
    """

    val: int

    def __post_init__(self):
        if not self.val & (self.val - 1) == 0:
            raise ValueError("Value must be 0 or a power of 2")


@dataclass(frozen=True)
class BeatDisplay:
    base_duration: BaseDuration
    """The base duration used to set notehead and rest glyphs"""

    dot_count: int
    """The number of flags required"""

    @property
    def flag_count(self) -> int:
        """Flag and beam count needed if used in a note"""
        if self.base_duration.val <= 4:
            return 0
        return int(math.log2(self.base_duration.val) - 2)
