from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.point import Point, PointDef
from neoscore.western.duration import Duration, DurationDef
from neoscore.western.duration_display import DurationDisplay

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class Rest(MusicText):

    """A simple Rest glyph whose appearance is determined by a duration

    Currently, the following rest types are not supported:
        * restHalfLegerLine
        * restWholeLegerLine
        * restLonga
        * restMaxima
    """

    _glyphnames = {
        1024: "rest1024th",
        512: "rest512th",
        256: "rest256th",
        128: "rest128th",
        64: "rest64th",
        32: "rest32nd",
        16: "rest16th",
        8: "rest8th",
        4: "restQuarter",
        2: "restHalf",
        1: "restWhole",
    }

    def __init__(
        self,
        pos: PointDef,
        parent: Parent,
        duration: DurationDef,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            pos: The position of the rest from its SMuFL anchor point
            parent: The parent of the rest. If no font is provided,
                this parent or one of its ancestors must implement `HasStaffUnit`.
            duration: `Duration` determining the particular rest glyph used.
            font: If provided, this overrides any font inherited from an ancestor.
        """
        pos = Point.from_def(pos)
        self.duration = Duration.from_def(duration)
        duration_display = cast(DurationDisplay, self.duration.display)
        MusicText.__init__(
            self,
            pos,
            parent,
            [self._glyphnames[duration_display.base_duration]],
            font,
        )

    ######## PUBLIC PROPERTIES ########

    @property
    def duration(self) -> Duration:
        """The time duration of this Rest"""
        return self._duration

    @duration.setter
    def duration(self, value: DurationDef):
        value = Duration.from_def(value)
        if value.display is None:
            raise ValueError(f"{value} cannot be represented as a single note")
        self._duration = value
