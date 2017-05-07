from brown.core.path import Path
from brown.core.pen import Pen
from brown.core.staff_object import StaffObject
from brown.utils.math_helpers import sign


class Stem(Path, StaffObject):

    """A vertical note/chord stem."""

    def __init__(self, start, height, parent):
        """
        Args:
            start (Point(StaffUnit)): Starting point for the stem
            height (StaffUnit): The height of the stem,
                where positive extend downward.
            parent (StaffObject or Staff):
        """
        Path.__init__(self, start, parent=parent)
        StaffObject.__init__(self, parent=parent)
        thickness = (
            self.staff.music_font.engraving_defaults['stemThickness'])
        self.pen = Pen(thickness=thickness)

        self._height = height
        # Draw stem path
        self.line_to(self.staff.unit(0), self.height)

    ######## PUBLIC PROPERTIES ########

    @property
    def height(self):
        """StaffUnit: The height of the stem from its position.

        Positive values extend downward, and vice versa.
        """
        return self._height

    @property
    def direction(self):
        """int: The direction the stem points, where -1 is up and 1 is down"""
        return sign(self.height)

    @property
    def start_point(self):
        """PathElement: The inner point; attached to a `Notehead`."""
        return self.elements[0]

    @property
    def end_point(self):
        """PathElement: The outer point; not attached to a `Notehead`."""
        return self.elements[1]
