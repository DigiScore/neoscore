from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.models.directions import VerticalDirection
from neoscore.models.duration import Duration, DurationDef
from neoscore.models.duration_display import DurationDisplay
from neoscore.utils.exceptions import NoFlagNeededError
from neoscore.utils.point import PointDef

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class Flag(MusicText):

    """A simple Flag glyph with a duration and direction"""

    _up_glyphnames = {
        8: "flag1024thUp",
        7: "flag512thUp",
        6: "flag256thUp",
        5: "flag128thUp",
        4: "flag64thUp",
        3: "flag32ndUp",
        2: "flag16thUp",
        1: "flag8thUp",
    }
    _down_glyphnames = {
        8: "flag1024thDown",
        7: "flag512thDown",
        6: "flag256thDown",
        5: "flag128thDown",
        4: "flag64thDown",
        3: "flag32ndDown",
        2: "flag16thDown",
        1: "flag8thDown",
    }

    def __init__(
        self,
        pos: PointDef,
        parent: Parent,
        duration: Duration,
        direction: VerticalDirection,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            pos: The position of this flag. When `parent` is a stem end point
                this should typically be `ORIGIN`.
            parent: If no font is given, this or one of its ancestors must
                implement `HasMusicFont`.
            duration: The duration corresponding to the flag. This controls the flag
                glyph rendered.
            direction: The direction of the flag
            font: If provided, this overrides any font found in the ancestor chain.
        """
        self.duration = duration
        self.direction = direction
        duration_display = cast(DurationDisplay, self.duration.display)
        if duration_display.flag_count == 0:
            raise NoFlagNeededError(self.duration)
        if self.direction == 1:
            glyph_name = self._down_glyphnames[duration_display.flag_count]
        else:
            glyph_name = self._up_glyphnames[duration_display.flag_count]
        MusicText.__init__(self, pos, parent, [glyph_name])

    ######## PUBLIC PROPERTIES ########

    @property
    def duration(self) -> Duration:
        """Duration: The time duration of this Notehead"""
        return self._duration

    @duration.setter
    def duration(self, value: DurationDef):
        value = Duration.from_def(value)
        if value.display is None:
            raise ValueError(f"{value} cannot be represented as a single note")
        self._duration = value

    @property
    def direction(self) -> VerticalDirection:
        """The flag direction"""
        return self._direction

    @direction.setter
    def direction(self, value: VerticalDirection):
        self._direction = value

    ######## PUBLIC CLASS METHODS ########

    @classmethod
    def vertical_offset_needed(cls, duration: Duration) -> int:
        """Find the space needed in a stem using a flag of a given duration

        Returns: a number to be plugged into a staff unit
        """
        # TODO LOW I believe this should become longer according to
        # division (and thus number of flaglets)
        if duration.display is None:
            return 0
        elif duration.display.flag_count:
            return 1
        else:
            return 0
