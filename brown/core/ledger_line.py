from brown.core.graphic_object import GraphicObject
from brown.core.path import Path
from brown.core.pen import Pen
from brown.core.staff_object import StaffObject
from brown.utils.point import PointDef
from brown.utils.units import Unit


class LedgerLine(Path, StaffObject):

    """A horizontal ledger line.

    These are generated automatically by `Chordrest` objects,
    but can be manually instantiated as well.
    """

    def __init__(self, pos: PointDef, parent: GraphicObject, base_length: Unit):
        """
        Args:
            pos: The position of the left edge of the notehead column.
            parent: The parent, which must be a staff or in one.
            base_length: The of the notehead this line is related to.
                The real length will be this plus a small extension defined in the
                `MusicFont`s engraving defaults.
        """
        Path.__init__(self, pos, parent=parent)
        StaffObject.__init__(self, parent=parent)
        thickness = self.staff.music_font.engraving_defaults["legerLineThickness"]
        self.pen = Pen(thickness=thickness)
        extension = self.staff.music_font.engraving_defaults["legerLineExtension"]
        length = base_length + extension
        self.move_to(extension * -1, self.staff.unit(0))
        self.line_to(length, self.staff.unit(0))
