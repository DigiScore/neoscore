from typing import Iterable, List, Optional

from neoscore.core.break_hint import BreakHint
from neoscore.core.color import ColorDef
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_font import MusicFont
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.point import ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Union, Unit
from neoscore.western import barline_style
from neoscore.western.abstract_staff import AbstractStaff
from neoscore.western.barline_style import BarlineStyle
from neoscore.western.multi_staff_object import MultiStaffObject
from neoscore.western.staff_group import StaffGroup

_DEFAULT_BARLINE_STYLE = BarlineStyle()


class Barline(PositionedObject, MultiStaffObject, HasMusicFont):
    """A barline spanning any number of staves.

    In addition to a default plain barline, this supports many common barline styles out
    of the box, and beyond those you can easily define custom barline styles.

    A :obj:`.BreakHint` is automatically attached to the end of the barline so
    :obj:`.Flowable` containers will treat barlines as potential line break points.
    """

    def __init__(
        self,
        pos_x: Unit,
        staves: Union[StaffGroup, List[AbstractStaff]],
        styles: Union[BarlineStyle, Iterable[BarlineStyle]] = barline_style.SINGLE,
        connected: Optional[bool] = True,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            pos_x: The barline X position relative to the highest staff.
                Specifies right edge of the barline group and offsets 'thickness'.
            staves: The staves spanned. If a raw list of staves is given, it must be
                in descending order.
            styles: This accepts any of the pre-made styles provided in
                :obj:`.barline_style`, in addition to custom styles defined in
                a list of :obj:`.BarlineStyle`\ s (one for each sub-barline).
            connected: Whether to connect the barline between staves.
            font: If provided, this overrides the font in the parent (top) staff.
        """
        MultiStaffObject.__init__(self, staves)
        PositionedObject.__init__(self, (pos_x, ZERO), self.highest)

        if font is None:
            font = HasMusicFont.find_music_font(self.highest)
        self._music_font = font
        self.engraving_defaults = self._music_font.engraving_defaults
        self.paths = []
        self.connected = connected

        # Start x position for first barline relative to self
        start_x = ZERO

        if isinstance(styles, BarlineStyle):
            styles = [styles]

        fallback_thickness = self.unit(_DEFAULT_BARLINE_STYLE.thickness)
        fallback_gap_right = self.unit(_DEFAULT_BARLINE_STYLE.gap_right)

        # draw each of the bar lines in turn from left to right
        for i in reversed(range(len(styles))):
            style = styles[i]
            thickness = self._resolve_style_measurement(
                style.thickness, fallback_thickness
            )
            # adjust start x to accommodate pen thickness
            start_x -= thickness / 2
            self._draw_barline(start_x, thickness, style.pattern, style.color)
            # move to next line to the left
            if i != 0:
                start_x -= thickness + self._resolve_style_measurement(
                    styles[i - 1].gap_right, fallback_gap_right
                )

        # Attach a break hint at the edge of the rightmost barline
        self._break_hint = BreakHint(ORIGIN, self)

    @property
    def music_font(self) -> MusicFont:
        return self._music_font

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
                ZERO, self.map_to(self.lowest).y + self.lowest.barline_extent[1]
            )

        else:
            y_offset = self.highest.y
            for stave in self.staves:
                new_y = stave.pos.y - y_offset
                line_path.move_to(ZERO, new_y + stave.barline_extent[0])
                line_path.line_to(ZERO, new_y + stave.barline_extent[1])

        self.paths.append(line_path)

    def _resolve_style_measurement(
        self, value: Union[str, float, Unit], fallback: Unit
    ) -> Unit:
        if isinstance(value, Unit):
            return value
        elif isinstance(value, (int, float)):
            return self.unit(value)
        else:
            return self.engraving_defaults.get(value, fallback)
