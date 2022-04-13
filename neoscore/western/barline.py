from typing import Optional

from neoscore.core.mapping import map_between_x
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import Pen, PenDef
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.path import Path

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
        style: Optional[BarLineStyle] = None,
        connected: Optional[bool] = True,
    ):
        """
        Args:
            pos_x: The barline X position relative to the highest staff.
            staves: The staves spanned. Must be in visually descending order.
            font: If provided, this overrides the font in the parent (top) staff.
            style: If provided, this declares the style of bar line e.g. double, end.
            connected: If provided, this declares if the bar lines are separated across a stave system
        """
        MultiStaffObject.__init__(self, staves)
        MusicPath.__init__(self, (pos_x, ZERO), self.highest, font)
        engraving_defaults = self.music_font.engraving_defaults
        separation = engraving_defaults["barlineSeparation"]
        self.pos_x = pos_x
        self.font = font

        # Calculate offset
        self.offset_x = self._calculate_offset()
        self.highest_stave = self.highest
        self.lowest_stave = self.lowest
        self.lowest_height = self.lowest.height

        if style:
            get_separation = engraving_defaults.get(style.separation)
            # if thinThick separation value not listed in this font
            # open normal value up a bit
            if not get_separation and style.separation == "thinThickBarlineSeparation":
                separation *= 1.5
                print('here')

            # draw each of the bar lines in turn from left to right
            for n, l in enumerate(style.lines):
                pattern = style.pattern
                thickness = engraving_defaults[style.lines[n]]
                self._draw_barline(self.pos_x,
                                   pattern,
                                   thickness)
                # # move to next line to the right
                self.pos_x += separation
        else:
            self._draw_barline(self.pos_x,
                               PenPattern.SOLID,
                               engraving_defaults["thinBarlineThickness"]
                               )

    #### PRIVATE METHODS ####
    def _draw_barline(self,
                      pos_x: Unit,
                      pen_pattern: PenPattern,
                      thickness: Unit
                      ):
        # Create the path
        pen = Pen(pattern=pen_pattern,
                  thickness=thickness)
        path = Path((pos_x, ZERO), self.highest, self.font, pen)

        # Draw the path
        bottom_x = pos_x + self.offset_x
        path.line_to(bottom_x,
                     self.lowest_height,
                     parent=self.lowest_stave)

    def _calculate_offset(self) -> Unit:
        # Calculate offset needed to make vertical line if top and
        # bottom staves are not horizontally aligned.
        return map_between_x(self.lowest, self.highest)
