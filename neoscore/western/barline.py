from typing import Optional

from neoscore.core.mapping import map_between_x
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import Pen, PenDef
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
        # todo - should this be deleted?
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
        MusicPath.__init__(self, (pos_x, ZERO), self.highest, font)
        engraving_defaults = self.music_font.engraving_defaults
        seperation = engraving_defaults["barlineSeparation"]
        self.pos_x = pos_x

        if style:
            for n, l in enumerate(style.lines):
                thickness = engraving_defaults[style.lines[n]]
                pen = Pen(pattern=style.pattern,
                               thickness=thickness)
                self.draw_bar_line(pen)
                self.move_to(Unit(seperation * n),
                             self.lowest.height,
                             parent=self.lowest)

        else:
            thickness = engraving_defaults["thinBarlineThickness"]
            self.pen = Pen(thickness=thickness)
            self.draw_bar_line(pen)

    def draw_bar_line(self, pen, separation=Unit(0)):
        # Draw the path
        # Calculate offset needed to make vertical line if top and
        # bottom staves are not horizontally aligned.
        offset_x = map_between_x(self.lowest, self.highest)
        self.bottom_x = self.pos_x + offset_x + separation
        self.line_to(self.bottom_x,
                     self.lowest.height,
                     parent=self.lowest)

    # @property
    # def pos_x(self):
    #     return self.pos_x


    # @property
    # def style(self):
    #     self.pen ==
    #
    #
    #     if self.style ==
    #
    #     self.thickness = self.engraving_defaults["thinBarlineThickness"]
    #
    #
    #     return self.thickness