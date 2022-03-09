from brown.core.graphic_object import GraphicObject
from brown.core.path import Path
from brown.core.path_element import PathElement
from brown.core.pen import Pen
from brown.core.staff_object import StaffObject
from brown.utils.math_helpers import sign
from brown.utils.point import ORIGIN, PointDef
from brown.utils.units import Unit


class Stem(Path, StaffObject):

    """A vertical note/chord stem."""

    def __init__(self, start: PointDef, height: Unit, parent: GraphicObject):
        """
        Args:
            start: Starting point for the stem
            height: The height of the stem,
                where positive extend downward.
            parent:
        """
        Path.__init__(self, start, parent=parent)
        StaffObject.__init__(self, parent=parent)
        thickness = self.staff.music_font.engraving_defaults["stemThickness"]
        self.pen = Pen(thickness=thickness)

        self._height = height
        # Draw stem path
        self.line_to(self.staff.unit(0), self.height)

    ######## PUBLIC PROPERTIES ########

    @property
    def height(self) -> Unit:
        """The height of the stem from its position.

        Positive values extend downward, and vice versa.
        """
        return self._height

    @property
    def direction(self) -> int:
        """The direction the stem points, where -1 is up and 1 is down"""
        return sign(self.height)

    @property
    def end_point(self) -> PathElement:
        """The outer point; not attached to a `Notehead`."""
        return self.elements[1]
