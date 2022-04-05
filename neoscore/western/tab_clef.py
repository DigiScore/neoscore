from __future__ import annotations

from typing import Optional

from neoscore.core import neoscore
from neoscore.core.brush import BrushDef
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.pen import PenDef
from neoscore.core.units import Unit
from neoscore.western.tab_staff import TabStaff


class TabClef(MusicText):

    """A "TAB" clef.

    Unlike classical clefs, this is purely cosmetic. It must be placed
    in a `TabStaff`, typically at the beginning. If the `TabStaff` is
    in a flowable, this automatically repeats at the beginning of
    every flowed staff line for the length of the staff. Because clef
    changes are generally inapplicable to tabs, clef changes are not
    currently supported.
    """

    def __init__(
        self,
        pos_x: Unit,
        staff: TabStaff,
        glyph_name: str = "6stringTabClef",
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
        hide_background: bool = True,
    ):
        """
        Args:
            pos_x: The x position relative to the parent
            staff: The parent staff
            glyph_name: The SMuFL glyph to use.
            font: The font to use. Defaults to the staff's font.
            brush: The brush to fill in text shapes with.
            pen: The pen to trace text outlines with. This defaults to no pen.
            hide_background: Whether to paint over the background behind the text.
        """
        MusicText.__init__(
            self,
            (pos_x, staff.center_y),
            staff,
            glyph_name,
            font,
            brush,
            pen,
            background_brush=neoscore.background_brush,
        )

    @property
    def breakable_length(self) -> Unit:
        return self.parent.breakable_length - self.x
