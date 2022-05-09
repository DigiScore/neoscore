from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Unit


class LedgerLine(Path, HasMusicFont):

    """A staff ledger line.

    These are generated automatically by :obj:`.Chordrest` objects,
    but can be manually instantiated as well.
    """

    def __init__(self, pos: PointDef, parent: PositionedObject, base_length: Unit):
        """
        Args:
            pos: A position at the left edge of the notehead column.
            parent: This or one of its ancestors must implement :obj:`.HasMusicFont`.
            base_length: The of the notehead this line is related to.
                The real length will be this plus a small extension defined in the
                :obj:`.MusicFont`'s engraving defaults.
        """
        Path.__init__(self, pos, parent=parent)
        font = self.music_font
        thickness = font.engraving_defaults["legerLineThickness"]
        self.pen = Pen(thickness=thickness)
        extension = font.engraving_defaults["legerLineExtension"]
        length = base_length + extension
        self.move_to(-extension, ZERO)
        self.line_to(length, ZERO)
