from typing import Optional

from neoscore.core.mapping import map_between_x
from neoscore.core.music_font import MusicFont
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import Pen, PenDef
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.path import Path
from neoscore.core.point import Point

from neoscore.core.units import ZERO, Unit
from neoscore.western.multi_staff_object import MultiStaffObject, StaffLike
from neoscore.western.barline_style import BarLineStyle

class Barline(PositionedObject, MultiStaffObject, HasMusicFont):

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
        # MusicPath.__init__(self, (pos_x, ZERO), self.highest, font)
        PositionedObject.__init__(self, (pos_x, ZERO),
                                  self.highest)

        if font is None:
            font = HasMusicFont.find_music_font(self.highest)
        self._music_font = font

        engraving_defaults = self.music_font.engraving_defaults
        separation = engraving_defaults["barlineSeparation"]
        # self.pos_x = self.x
        self.font = font
        self.paths = []

        # Calculate positions
        self.offset_x = self._calculate_offset()
        # self.highest_stave = self.highest
        # self.lowest_stave = self.lowest
        # self.lowest_height = self.lowest.height
        start_x = ZERO

        if style:
            get_separation = engraving_defaults.get(style.separation)
            # if thinThick separation value not listed in this font
            # open normal value up a bit
            # else it remains "barlineSeperation" value from above
            if not get_separation and style.separation == "thinThickBarlineSeparation":
                separation *= 1.5
                print('here')

            # draw each of the bar lines in turn from left to right
            for n, l in enumerate(style.lines):
                pattern = style.pattern
                thickness = engraving_defaults[style.lines[n]]
                self._draw_barline(start_x,
                                   pattern,
                                   thickness)
                # # move to next line to the right
                start_x += separation
        else:
            self._draw_barline(start_x,
                               PenPattern.SOLID,
                               engraving_defaults["thinBarlineThickness"]
                               )

    @property
    def music_font(self) -> MusicFont:
        return self._music_font

    #### PRIVATE METHODS ####
    def _draw_barline(self,
                      top_x: Unit,
                      pen_pattern: PenPattern,
                      thickness: Unit
                      ):
        # Create the path
        print(top_x)
        self.line_path = Path(
            Point(top_x, ZERO),
            self,
            pen=Pen(pattern=pen_pattern,
                    thickness=thickness)
        )

        # Draw the path
        bottom_x = self.x + top_x + self.offset_x
        self.line_path.line_to(bottom_x,
                               self.lowest.height,
                               parent=self.lowest)
        self.paths.append(self.line_path)

    def _calculate_offset(self) -> Unit:
        # Calculate offset needed to make vertical line if top and
        # bottom staves are not horizontally aligned.
        return map_between_x(self.lowest, self.highest)

