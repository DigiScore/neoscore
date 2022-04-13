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
        MusicPath.__init__(self, (pos_x, ZERO), self.highest, font)
        self.engraving_defaults = self.music_font.engraving_defaults
        self.separation = self.engraving_defaults["barlineSeparation"]
        self.pos_x = pos_x
        self.font = font

        # do we need an over-ride pen?
        self.pen = pen

        # Calculate offset
        self.offset_x = self._calculate_offset()
        self.highest_stave = self.highest
        self.lowest_stave = self.lowest
        self.lowest_height = self.lowest.height

        if style:
            get_separation = self.engraving_defaults.get(style.separation)
            print(get_separation)

            # if thinThick separation value not listed in this font
            # open normal value up a bit
            if get_separation == None and style.separation == "thinThickBarlineSeparation":
                self.separation *= 1.5

            # draw each of the bar lines in turn fro left to right
            for n, l in enumerate(style.lines):
                pattern = style.pattern
                thickness = style.lines[n]
                self._draw_bar_line(pattern,
                                    thickness)
        else:
            self._draw_bar_line()


    #### PRIVATE METHODS ####
    def _draw_bar_line(self,
                       pattern=PenPattern.SOLID,
                       thickness="thinBarlineThickness"
                       ):
        # Create the path
        path = Path((self.pos_x, ZERO), self.highest, self.font)
        thickness = self.engraving_defaults[thickness]
        path.pen = Pen(pattern=pattern,
                       thickness=thickness)
        bottom_x = self.pos_x + self.offset_x

        # Draw the path
        path.line_to(bottom_x,
                     self.lowest_height,
                     parent=self.lowest_stave)

        # move to next line to the right
        self.pos_x += self.separation

    def _calculate_offset(self):
        # Calculate offset needed to make vertical line if top and
        # bottom staves are not horizontally aligned.
        return map_between_x(self.lowest, self.highest)
