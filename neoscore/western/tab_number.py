from typing import List, Optional

from neoscore.core.brush import BrushDef
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import PenDef
from neoscore.core.units import Unit
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
        hide_background=True,
    ):
        """
        Args:
            pos_x: The x position relative to the parent
            staff: The parent staff
            string: The 1-indexed string number this should appear on
            number: The number to display. Must be a non-zero integer.
            font: The font to use. Defaults to the staff's font.
            brush: The brush to fill in text shapes with.
            pen: The pen to trace text outlines with. This defaults to no pen.
            hide_background: Whether to paint over the background behind the text.
                Particularly useful for preventing overlaps with staff lines.
        """
        TabStringText.__init__(
            self,
            pos_x,
            staff,
            string,
            TabNumber._number_to_digit_glyph_names(number),
            font,
            brush,
            pen,
            hide_background,
        )

    @staticmethod
    def _number_to_digit_glyph_names(number: int) -> List[str]:
        return [f"fingering{digit}" for digit in str(number)]
