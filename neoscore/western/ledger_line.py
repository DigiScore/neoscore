from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import Unit


class LedgerLine(Path, HasMusicFont):

    """A horizontal ledger line.

    These are generated automatically by `Chordrest` objects,
    but can be manually instantiated as well.
    """

    def __init__(self, pos: PointDef, parent: PositionedObject, base_length: Unit):
        """
        Args:
            pos: The position of the left edge of the notehead column.
            parent: The parent, which must be a staff or in one.
            base_length: The of the notehead this line is related to.
                The real length will be this plus a small extension defined in the
                `MusicFont`s engraving defaults.
        """
        Path.__init__(self, pos, parent=parent)
        font = self.music_font
        thickness = font.engraving_defaults["legerLineThickness"]
        self.pen = Pen(thickness=thickness)
        extension = font.engraving_defaults["legerLineExtension"]
        length = base_length + extension
        self.move_to(extension * -1, self.unit(0))
        self.line_to(length, self.unit(0))
