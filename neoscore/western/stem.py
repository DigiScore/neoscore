from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.path_element import PathElement
from neoscore.core.pen import Pen
from neoscore.models.directions import VerticalDirection
from neoscore.utils.math_helpers import sign
from neoscore.utils.point import PointDef
from neoscore.utils.units import ZERO, Unit

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent

# TODO MEDIUM maybe make this take a length and vertical direction?


class Stem(MusicPath):

    """A vertical note/chord stem.

    While this is a path, it requires a music font from which to
    derive its appearance.
    """

    def __init__(
        self,
        start: PointDef,
        parent: Parent,
        height: Unit,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            start: Starting point for the stem
            parent: If no font is given, this or one of its ancestors must
                implement `HasMusicFont`.
            height: The height of the stem, where positive extends
                downward and negative extends upward.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        MusicPath.__init__(self, start, parent, font=font)
        self.pen = Pen(thickness=self.music_font.engraving_defaults["stemThickness"])

        self._height = height
        # Draw stem path
        self.line_to(ZERO, self.height)

    ######## PUBLIC PROPERTIES ########

    @property
    def height(self) -> Unit:
        """The height of the stem from its position.

        Positive values extend downward, and vice versa.
        """
        return self._height

    @property
    def direction(self) -> VerticalDirection:
        """The direction the stem points, where -1 is up and 1 is down"""
        if sign(self.height) == 1:
            return VerticalDirection.DOWN
        else:
            return VerticalDirection.UP

    @property
    def end_point(self) -> PathElement:
        """The outer point; not attached to a `Notehead`."""
        return self.elements[1]
