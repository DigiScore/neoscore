from __future__ import annotations

from typing import TYPE_CHECKING, Union

from neoscore.core.music_text import MusicText
from neoscore.core.staff_object import StaffObject
from neoscore.models.beat import Beat, BeatDef
from neoscore.utils.point import Point, PointDef

if TYPE_CHECKING:
    from neoscore.core.staff import Staff


class Rest(MusicText, StaffObject):

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
        parent: Union[StaffObject, Staff],
        duration: BeatDef,
    ):
        pos = Point.from_def(pos)
        self._duration = Beat.from_def(duration)
        MusicText.__init__(self, pos, parent, [self._glyphnames[self.duration.base_division]])
        StaffObject.__init__(self, parent)

    ######## PUBLIC PROPERTIES ########

    @property
    def duration(self):
        """Beat: The time duration of this Rest"""
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value
