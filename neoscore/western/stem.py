from __future__ import annotations

from typing import Optional

from neoscore.core.directions import DirectionY
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.path_element import PathElement
from neoscore.core.pen import Pen
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Unit


class Stem(MusicPath):

    """A vertical note/chord stem.

    While this is a path, it requires a music font from which to
    derive its appearance.
    """

    def __init__(
        self,
        start: PointDef,
        parent: PositionedObject,
        direction: DirectionY,
        height: Unit,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            start: Starting point for the stem
            parent: If no font is given, this or one of its ancestors must
                implement ``HasMusicFont``.
            direction: The direction a stem points
            height: The height/ length of the stem.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        MusicPath.__init__(self, start, parent, font=font)
        self.pen = Pen(thickness=self.music_font.engraving_defaults["stemThickness"])

        self._direction = direction
        self._height = height
        # Draw stem path
        self.line_to(ZERO, self.height * self.direction.value)

    ######## PUBLIC PROPERTIES ########

    @property
    def height(self) -> Unit:
        """The height of the stem from its position.
        Must be positive value"""
        return self._height

    @property
    def direction(self) -> DirectionY:
        """The direction the stem points, where -1 is up and 1 is down"""
        return self._direction

    @property
    def end_point(self) -> PathElement:
        """The outer point; not attached to a ``Notehead``."""
        return self.elements[1]
