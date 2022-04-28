from collections.abc import Iterable
from typing import Optional

from neoscore.core.break_hint import BreakHint
from neoscore.core.color import ColorDef
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.mapping import map_between
from neoscore.core.music_font import MusicFont
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.point import Point, ORIGIN
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Union, Unit
from neoscore.western import barline_style
from neoscore.western.barline_style import BarlineStyle
from neoscore.western.multi_staff_object import MultiStaffObject, StaffLike


class Barline(PositionedObject, MultiStaffObject, HasMusicFont):
    """A barline.

    This is drawn as vertical lines at a given x coordinate
    spanning the full height of a series of staves.

    The style of the bar line is determined by the optional style
    value. If none then will resort to default single thin line.

    The thickness of the line is determined by the engraving defaults
    on the top staff. Can be over-ridden by the font property.

    A ``BreakHint`` is automatically attached to the end of the barline.
    """

    def __init__(
        self,
        pos_x: Unit,
        staves: list[StaffLike],
        styles: BarlineStyle | Iterable[BarlineStyle] = barline_style.SINGLE,
        font: Optional[MusicFont] = None,
        connected: Optional[bool] = True,
    ):
        """
        Args:
            pos_x: The barline X position relative to the highest staff.
                Specifies right edge of the barline group and offsets 'thickness'.
            staves: The staves spanned. Must be in visually descending order.
            styles: If provided, this accepts any of the premade styles provided in
                barline_style, in addition to custom styles created with BarlineStyle.
            font: If provided, this overrides the font in the parent (top) staff.
            connected: If provided, connects all barlines across the staves span (True)
        """
        MultiStaffObject.__init__(self, staves)
        PositionedObject.__init__(self, (pos_x, ZERO), self.highest)

        if font is None:
            font = HasMusicFont.find_music_font(self.highest)
        self._music_font = font
        self.engraving_defaults = self._music_font.engraving_defaults
        self.paths = []
        self.staves = staves
        self.connected = connected

        # Start x position for first barline relative to self
        start_x = ZERO

        if isinstance(styles, BarlineStyle):
            styles = [styles]

        # draw each of the bar lines in turn from left to right
        for style in reversed(styles):
            thickness = self._resolve_style_measurement(style.thickness)
            # adjust start x to accommodate pen thickness
            start_x -= thickness / 2
            self._draw_barline(start_x, thickness, style.pattern, style.color)
            # move to next line to the left
            start_x -= thickness + self._look_up_engraving_default(style.gap_right)

        # Attach a break hint at the edge of the rightmost barline
        # last_path = self.paths[0]
        self._break_hint = BreakHint(ORIGIN, self)

    @property
    def music_font(self) -> MusicFont:
        return self._music_font

    #### PRIVATE METHODS ####
    def _draw_barline(
        self, start_x: Unit, thickness: Unit, pen_pattern: PenPattern, color: ColorDef
    ):
        # Create the path
        line_path = Path(
            Point(start_x, ZERO),
            self,
            pen=Pen(pattern=pen_pattern, thickness=thickness, color=color),
        )

        # Draw the path
        if self.connected:
            line_path.move_to(ZERO, self.highest.barline_extent[0])
            line_path.line_to(
                ZERO, map_between(self, self.lowest).y + self.lowest.barline_extent[1]
            )

        else:
            y_offset = self.highest.y
            for stave in self.staves:
                new_y = stave.pos.y - y_offset
                line_path.move_to(ZERO, new_y + stave.barline_extent[0])
                line_path.line_to(ZERO, new_y + stave.barline_extent[1])

        self.paths.append(line_path)

    def _resolve_style_measurement(self, thickness: Union[str, float, Unit]) -> Unit:
        if type(thickness) == Unit:
            return thickness
        elif type(thickness) == str:
            return self.engraving_defaults[thickness]
        else:
            return Unit(thickness)

    def _look_up_engraving_default(self, gap: Union[str, float, Unit]) -> Unit:
        # Get separation value from engraving defaults if listed
        if type(gap) == Unit:
            return gap
        elif type(gap) == float:
            return Unit(gap)
        else:
            value = self.engraving_defaults.get(gap)
            if value:
                return value
            else:
                return self.engraving_defaults["barlineSeparation"]
