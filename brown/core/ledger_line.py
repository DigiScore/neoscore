from brown.core.path import Path
from brown.core.pen import Pen
from brown.core.staff_object import StaffObject


class LedgerLine(Path, StaffObject):

    """A horizontal ledger line.

    These are generated automatically by `Chordrest` objects,
    but can be manually instantiated as well.
    """

    def __init__(self, pos, parent, base_length):
        """
        Args:
            pos (Point(StaffUnit)): The position of the left edge of
                the notehead column.
            parent (StaffObject or Staff):
            base_length (StaffUnit): The of the notehead this line
                is related to. The real length will be this plus a small
                extension defined in the `MusicFont`s engraving defaults.
        """
        Path.__init__(self, pos, parent=parent)
        StaffObject.__init__(self, parent=parent)
        thickness = (
            self.staff.music_font.engraving_defaults['legerLineThickness'])
        self.pen = Pen(thickness=thickness)
        extension = (
            self.staff.music_font.engraving_defaults['legerLineExtension'])
        length = base_length + extension
        self.move_to(extension * -1, self.staff.unit(0))
        self.line_to(length, self.staff.unit(0))
