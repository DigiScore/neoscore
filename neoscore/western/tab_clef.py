from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.utils.units import Unit
from neoscore.western.tab_staff import TabStaff

if TYPE_CHECKING:
    pass


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
    ):
        """
        Args:
            pos_x: The x position relative to the parent
            staff: The parent staff
            glyph_name: The SMuFL glyph to use.
            font: The font to use. Defaults to the staff's font.
        """
        MusicText.__init__(self, (pos_x, staff.center_y), staff, glyph_name, font)

    @property
    def breakable_length(self) -> Unit:
        return self.parent.breakable_length - self.x
