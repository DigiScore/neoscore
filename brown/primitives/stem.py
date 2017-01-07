from brown.core.pen import Pen
from brown.core.path import Path
from brown.primitives.staff_object import StaffObject


class Stem(Path, StaffObject):

    def __init__(self, start, height, parent, music_font=None):
        """
        Args:
            start (Point(StaffUnit)): Starting point for the stem
            height (StaffUnit): The height of the stem,
                where positive extend downward.
            parent (StaffObject or Staff):
            music_font (MusicFont): An optional font to be passed
                which is used to determine the ideal stem thickness.
        """
        Path.__init__(self, start, parent=parent)
        StaffObject.__init__(self, parent=parent)
        if music_font:
            thickness = self.staff.unit(
                music_font.engraving_defaults['stemThickness'])
        else:
            thickness = None
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
