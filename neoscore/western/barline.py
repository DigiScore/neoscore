from typing import Optional

from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.mapping import map_between_x
from neoscore.core.music_font import MusicFont
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.point import Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Unit
from neoscore.western.barline_style import BarlineStyle, SINGLE
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
        font: Optional[MusicFont] = None,
        style: BarlineStyle = SINGLE,
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
        self.style = style
        self.paths = []

        # Calculate positions for this object
        start_x = ZERO
        # offset_x = self._calculate_offset()
        # bottom_x = start_x # self.x + offset_x

        # if style:
            # determine a special case for separation
            # separation = self._calculate_separation()

            # draw each of the bar lines in turn from left to right
        for n, l in enumerate(style.thickness):
            if n > 0:
                # move to next line to the right
                start_x += style.gap_right
                # bottom_x += separation

            pattern = style.pattern
            thickness = style.thickness # self.engraving_defaults[style.lines[n]]
            color = style.color
            self._draw_barline(start_x, pattern, thickness, color)
        # else:
        #     self._draw_barline(
        #         start_x,
        #         bottom_x,
        #         PenPattern.SOLID,
        #         self.engraving_defaults["thinBarlineThickness"],
        #     )

    @property
    def music_font(self) -> MusicFont:
        return self._music_font

    #### PRIVATE METHODS ####
    def _draw_barline(
        self, x: Unit,
            pen_pattern: PenPattern,
            thickness: Unit,
    ):
        # Create the path

        line_path = Path(
            Point(x, ZERO),
            self,
            pen=Pen(pattern=pen_pattern, thickness=thickness),
        )
        line_path.move_to(ZERO, self.highest.barline_extent[0])

        # Draw the path
        line_path.line_to(x, self.lowest.height, parent=self.lowest)
        self.paths.append(line_path)

    # def _calculate_offset(self) -> Unit:
    #     # Calculate offset needed to make vertical line if top and
    #     # bottom staves are not horizontally aligned.
    #     return map_between_x(self.lowest, self.highest)

    def _calculate_separation(self) -> Unit:
        # Get separation value from engraving defaults if listed
        get_separation = self.engraving_defaults.get(self.style.gap_right)
        if get_separation:
            return get_separation
        # but if thinThick separation value not listed in this font
        # return home-made thinThick = normal default value * 2
        elif (
            not get_separation and self.style.separation == "thinThickBarlineSeparation"
        ):
            return self.engraving_defaults["barlineSeparation"] * 2
        # else return normal "barlineSeparation"
        else:
            return self.engraving_defaults["barlineSeparation"]
