from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.directions import VerticalDirection
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.path_element import PathElement
from neoscore.core.pen import Pen
from neoscore.utils.point import PointDef
from neoscore.utils.units import ZERO, Unit

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class Stem(MusicPath):

    """A vertical note/chord stem.

    While this is a path, it requires a music font from which to
    derive its appearance.
    """

    def __init__(
        self,
        start: PointDef,
        parent: Parent,
        direction: VerticalDirection,
        height: Unit,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            start: Starting point for the stem
            parent: If no font is given, this or one of its ancestors must
                implement `HasMusicFont`.
            direction: The direction a stem points:
                verticalDirection.UP or .DOWN
            height: The height/ length of the stem.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        MusicPath.__init__(self, start, parent, font=font)
        self.pen = Pen(thickness=self.music_font.engraving_defaults["stemThickness"])

        self._direction = direction
        self._height = height
        # Draw stem path
        self.line_to(ZERO, (self.height * self.direction.value))

    ######## PUBLIC PROPERTIES ########

    @property
    def height(self) -> Unit:
        """The height of the stem from its position."""
        return self._height

    @property
    def direction(self) -> VerticalDirection:
        """The direction the stem points, where -1 is up and 1 is down"""
        return self._direction

    @property
    def end_point(self) -> PathElement:
        """The outer point; not attached to a `Notehead`."""
        return self.elements[1]
