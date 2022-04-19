from typing import Optional

from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.mapping import map_between_x
from neoscore.core.music_font import MusicFont
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.color import ColorDef
from neoscore.core.point import Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Unit, Union
from neoscore.western import barline_style
from neoscore.western.barline_style import BarlineStyle
from neoscore.western.multi_staff_object import MultiStaffObject, StaffLike


class Barline(PositionedObject, MultiStaffObject, HasMusicFont):
    """A bar line.

    This is drawn as vertical lines at a given x coordinate
    spanning the full height of a series of staves.

    The style of the bar line is determined by the optional style
    value. If none then will resort to default single thin line.

    The thickness of the line is determined by the engraving defaults
    on the top staff. Can be over-ridden by the font property.
    """

    def __init__(
        self,
        pos_x: Unit,
        staves: list[StaffLike],
        style: tuple[BarlineStyle] = barline_style.SINGLE,
        font: Optional[MusicFont] = None,
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
        PositionedObject.__init__(self, (pos_x, ZERO), self.highest)

        if font is None:
            font = HasMusicFont.find_music_font(self.highest)
        self._music_font = font
        self.engraving_defaults = self.music_font.engraving_defaults
        self.paths = []

        # State x position for this object relative to self
        start_x = ZERO

        # draw each of the bar lines in turn from left to right
        for n, bl in enumerate(style):
            print(n, style)
            if type(bl.thickness) == str:
                thickness = self.engraving_defaults[bl.thickness]
            else:
                thickness = bl.thickness

            self._draw_barline(start_x,
                               thickness,
                               bl.pattern,
                               bl.color
                               )

            # move to next line to the right
            if len(style) > 1:
                # todo - this is not elegant, but Union is complaining
                if type(bl.gap_right) == str:
                    start_x += self._calculate_separation(bl.gap_right)    # self.engraving_defaults[bl.gap_right]
                elif type(bl.gap_right) == float:
                    start_x += Unit(bl.gap_right)
                else:
                    start_x += bl.gap_right

    @property
    def music_font(self) -> MusicFont:
        return self._music_font

    #### PRIVATE METHODS ####
    def _draw_barline(
        self, start_x: Unit,
            thickness: Unit,
            pen_pattern: PenPattern,
            color: ColorDef
    ):
        # Create the path
        line_path = Path(
            Point(start_x, ZERO),
            self,
            pen=Pen(pattern=pen_pattern, thickness=thickness, color=color),
        )
        # move to counter the barline extant offset
        line_path.move_to(ZERO, self.highest.barline_extent[0])

        # Draw the path
        line_path.line_to(ZERO,
                          self.vertical_span - self.lowest.height + self.lowest.barline_extent[1])
        self.paths.append(line_path)

    # def _calculate_offset(self) -> Unit:
    #     # Calculate offset needed to make vertical line if top and
    #     # bottom staves are not horizontally aligned.
    #     return map_between_x(self.lowest, self.highest)

    def _calculate_separation(self, gap_right) -> Unit:
        # Get separation value from engraving defaults if listed
        get_separation = self.engraving_defaults.get(gap_right)
        if get_separation:
            return get_separation
        else:
            return self.engraving_defaults["barlineSeparation"]
