from typing import Optional

from neoscore.core import neoscore
from neoscore.core.brush import BrushDef
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicStringDef, MusicText
from neoscore.core.pen import PenDef
from neoscore.core.text_alignment import AlignmentX, AlignmentY
from neoscore.core.units import Unit
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
        text: MusicStringDef,
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
        hide_background: bool = True,
        breakable: bool = True,
        alignment_x: AlignmentX = AlignmentX.CENTER,
        alignment_y: AlignmentY = AlignmentY.CENTER,
    ):
        """
        Args:
            pos_x: The x position relative to the parent. The text will be
                centered around this position.
            staff: The parent staff
            string: The 1-indexed string number this should appear on
            text: The text to display. Can be given as a SMuFL glyph name,
                or other shorthand forms. See :obj:`.MusicStringDef`.
            font: The font to use. Defaults to the staff's font.
            brush: The brush to fill in text shapes with.
            pen: The pen to trace text outlines with. This defaults to no pen.
            hide_background: Whether to paint over the background behind the text.
                Particularly useful for preventing overlaps with staff lines.
            breakable: Whether this object should break across lines in
                Flowable containers.
            alignment_x: The text's horizontal alignment relative to ``pos``.
                Note that the default value here is center-alignment, unlike
                most other text classes.
            alignment_y: The text's vertical alignment relative to ``pos``.
                Note that the default value here is center-alignment, unlike
                most other text classes.
        """
        background_brush = neoscore.background_brush if hide_background else None
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
            0,
            background_brush,
            breakable,
            alignment_x,
            alignment_y,
        )
