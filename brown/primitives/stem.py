from brown.core.pen import Pen
from brown.core.path import Path
from brown.primitives.staff_object import StaffObject


class Stem(Path, StaffObject):

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
            self.staff.default_music_font.engraving_defaults['stemThickness'])
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
