from brown.core.path import Path
from brown.core.pen import Pen
from brown.core.staff_object import StaffObject


class LedgerLine(Path, StaffObject):

    def __init__(self, pos, parent, base_length):
        """
        Args:
            pos (Point(StaffUnit)): The position of the left edge of
                the notehead column.
            parent (StaffObject or Staff):
            base_length (StaffUnit): Length of the ledger line
        """
        Path.__init__(self, pos, parent=parent)
        StaffObject.__init__(self, parent=parent)
        thickness = (
            self.staff.music_font.engraving_defaults['legerLineThickness'])
        self.extension = (
            self.staff.music_font.engraving_defaults['legerLineExtension'])
        self.pen = Pen(thickness=thickness)
        self.base_length = base_length
        self.move_to(self.extension * -1, self.staff.unit(0))
        self.line_to(self.length, self.staff.unit(0))

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self):
        """Unit: The length of the ledger line"""
        return self.base_length + (self.extension)
