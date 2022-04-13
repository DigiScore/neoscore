from typing import Optional

from neoscore.core.mapping import map_between_x
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import Pen, PenDef
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.units import ZERO, Unit
from neoscore.western.multi_staff_object import MultiStaffObject, StaffLike
from neoscore.western.barline_style import BarLineStyle

class Barline(MusicPath, MultiStaffObject):

    """A single bar line.

    This is drawn as a single vertical line at a given x coordinate
    spanning the full height of a series of staves.

    The thickness of the line is determined by the engraving defaults
    on the top staff.
    """

    def __init__(
        self,
        pos_x: Unit,
        staves: list[StaffLike],
        font: Optional[MusicFont] = None,
        # todo - should pen be deleted?
        pen: Optional[PenDef] = None,
        style: Optional[BarLineStyle] = None,
        connected: Optional[bool] = True,
    ):
        """
        Args:
            pos_x: The barline X position relative to the highest staff.
            staves: The staves spanned. Must be in visually descending order.
            font: If provided, this overrides the font in the parent (top) staff.
            pen: The pen used to draw the path. Defaults to a pen with
                thickness from the music font's engraving default.
            style:
        """
        MultiStaffObject.__init__(self, staves)
        # MusicPath.__init__(self, (pos_x, ZERO), self.highest, font)
        # engraving_defaults = self.music_font.engraving_defaults
        # self.separation = engraving_defaults["barlineSeparation"]
        self.pos_x = pos_x
        self.font = font

        # do we need an over-ride pen?
        self.pen = pen

        # Calculate offset needed to make vertical line if top and
        # bottom staves are not horizontally aligned.
        self.offset_x = self.calculate_offset()

        if style:
            for n, l in enumerate(style.lines):
                pattern = style.pattern
                thickness = style.lines[n]
                self.draw_bar_line(n,
                                   pattern,
                                   thickness)

                # move to next line to the right
                # self.move_to(self.separation,
                #              ZERO)
                # self.pos_x += self.separation * 3

        else:
            # MusicPath.__init__(self, (pos_x, ZERO), self.highest, font)
            # thickness = engraving_defaults["thinBarlineThickness"]
            # self.pen = Pen(thickness=thickness)
            self.draw_bar_line()

    def draw_bar_line(self, line_number=0, pattern=PenPattern.SOLID, thickness="thinBarlineThickness"):
        # Draw the path
        MusicPath.__init__(self, (self.pos_x, ZERO), self.highest, self.font)
        engraving_defaults = self.music_font.engraving_defaults
        self.separation = engraving_defaults["barlineSeparation"]
        thickness = engraving_defaults[thickness]
        self.pen = Pen(pattern=pattern,
                       thickness=thickness)

        self.bottom_x = self.pos_x + self.offset_x + (self.separation * line_number)
        self.line_to(self.bottom_x,
                     self.lowest.height,
                     parent=self.lowest)

    def calculate_offset(self):
        # Calculate offset needed to make vertical line if top and
        # bottom staves are not horizontally aligned.
        return map_between_x(self.lowest, self.highest)
