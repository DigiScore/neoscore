from typing import Optional

from neoscore.core.brush import BrushDef
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import PenDef
from neoscore.utils.units import Unit
from neoscore.western.tab_staff import TabStaff
from neoscore.western.tab_string_text import TabStringText


class TabNumber(TabStringText):
    """A number placed in a tab staff typically used to indicate frets or fingers"""

    def __init__(
        self,
        pos_x: Unit,
        staff: TabStaff,
        string: int,
        number: int,
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        # TODO HIGH support multiple digits, can be done easily with music char input list.
        TabStringText.__init__(
            self, pos_x, staff, string, f"fingering{number}", font, brush, pen
        )
