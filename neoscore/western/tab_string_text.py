from typing import Any, Optional, cast

from neoscore.core import neoscore
from neoscore.core.brush import BrushDef
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.pen import PenDef
from neoscore.utils.units import Unit
from neoscore.western.tab_staff import TabStaff


class TabStringText(MusicText):
    """SMuFL text centered on a tab staff line.

    This also automatically adds a background brush which hides the
    tab staff line behind the text.
    """

    def __init__(
        self,
        pos_x: Unit,
        staff: TabStaff,
        string: int,
        text: Any,
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
        breakable: bool = True,
    ):
        pos_y = staff.string_y(string)
        MusicText.__init__(
            self,
            (pos_x, pos_y),
            staff,
            text,
            font,
            brush,
            pen,
            1,
            neoscore.background_brush,
            breakable,
        )
        self.y = pos_y + cast(Unit, self.bounding_rect.height / 2)
