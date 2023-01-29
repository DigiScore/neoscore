from __future__ import annotations

from typing import Optional

from neoscore.core import neoscore
from neoscore.core.brush import Brush, BrushDef
from neoscore.core.font import Font
from neoscore.core.layout_controllers import NewLine
from neoscore.core.painted_object import PaintedObject
from neoscore.core.pen import Pen, PenDef
from neoscore.core.point import ORIGIN, Point, PointDef
from neoscore.core.positioned_object import PositionedObject, render_cached_property
from neoscore.core.rect import Rect
from neoscore.core.text_alignment import AlignmentX, AlignmentY
from neoscore.core.units import ZERO, Unit
from neoscore.interface.text_interface import TextInterface


class Text(PaintedObject):

    """A graphical text object."""

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
        text: str,
        font: Optional[Font] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
        scale: float = 1,
        rotation: float = 0,
        background_brush: Optional[BrushDef] = None,
        breakable: bool = True,
        alignment_x: AlignmentX = AlignmentX.LEFT,
        alignment_y: AlignmentY = AlignmentY.BASELINE,
        transform_origin: PointDef = ORIGIN,
    ):
        """
        Args:
            pos: Position relative to the parent
            parent: The parent object. Defaults to the document's first page.
            text: The text to be displayed
            font: The font to display the text in.
            brush: The brush to fill in text shapes with.
            pen: The pen to trace text outlines with. This defaults to no pen.
            scale: A scaling factor relative to the font size.
            rotation: Angle in degrees. Note that breakable rotated text is
                not currently supported.
            background_brush: Optional brush used to paint the text's bounding rect
                behind it.
            breakable: Whether this object should break across lines in
                :obj:`.Flowable` containers.
            alignment_x: The text's horizontal alignment relative to ``pos``.
                Note that text which is not ``LEFT`` aligned does not currently display
                correctly when breaking across flowable lines.
            alignment_y: The text's vertical alignment relative to ``pos``.
            transform_origin: The origin point for rotation and scaling transforms
        """
        super().__init__(pos, parent, brush, pen or Pen.no_pen())
        if font:
            self._font = font
        else:
            self._font = neoscore.default_font
        self._text = text
        self._scale = scale
        self._rotation = rotation
        self.background_brush = background_brush
        self._breakable = breakable
        self._alignment_x = alignment_x
        self._alignment_y = alignment_y
        self.transform_origin = transform_origin

    @property
    def breakable_length(self) -> Unit:
        """The breakable length of the object.

        This is used to determine how and where rendering cuts should be made.

        This is derived from other properties and cannot be set directly.
        """
        if self.breakable:
            return self.bounding_rect.width + self._alignment_offset.x
        else:
            return ZERO

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

    @property
    def font(self) -> Font:
        return self._font

    @font.setter
    def font(self, value: Font):
        self._font = value

    @property
    def background_brush(self) -> Optional[Brush]:
        """The brush to paint over the background with."""
        return self._background_brush

    @background_brush.setter
    def background_brush(self, value: Optional[BrushDef]):
        if value:
            self._background_brush = Brush.from_def(value)
        else:
            self._background_brush = None

    @property
    def breakable(self) -> bool:
        """Whether this object should be broken across flowable lines."""
        return self._breakable

    @breakable.setter
    def breakable(self, value: bool):
        self._breakable = value

    @property
    def alignment_x(self) -> AlignmentX:
        """The text's horizontal alignment relative to ``pos``.

        Note that text which is not ``LEFT`` aligned does not currently display
        correctly when breaking across flowable lines.
        """
        return self._alignment_x

    @alignment_x.setter
    def alignment_x(self, value: AlignmentX):
        self._alignment_x = value

    @property
    def alignment_y(self) -> AlignmentY:
        """The text's vertical alignment relative to ``pos``."""
        return self._alignment_y

    @alignment_y.setter
    def alignment_y(self, value: AlignmentY):
        self._alignment_y = value

    @render_cached_property
    def _alignment_offset(self) -> Point:
        if (
            self.alignment_x == AlignmentX.LEFT
            and self.alignment_y == AlignmentY.BASELINE
        ):
            return ORIGIN
        x = ZERO
        y = ZERO
        bounding_rect = self._raw_scaled_bounding_rect
        if self.alignment_x == AlignmentX.CENTER:
            x = (bounding_rect.width / -2) - bounding_rect.x
        elif self.alignment_x == AlignmentX.RIGHT:
            x = -bounding_rect.width - bounding_rect.x
        if self.alignment_y == AlignmentY.CENTER:
            y = (bounding_rect.height / -2) - bounding_rect.y
        return Point(x, y)

    @render_cached_property
    def _raw_scaled_bounding_rect(self) -> Rect:
        """The text bounding rect without centering adjustment"""
        return self.font.bounding_rect_of(self.text) * self.scale

    @render_cached_property
    def bounding_rect(self) -> Rect:
        """The bounding rect for this text positioned relative to ``pos``.

        The rect ``(x, y)`` position is relative to the object's position.

        Note that this currently accounts for scaling, but not rotation.
        """
        raw_rect = self._raw_scaled_bounding_rect
        alignment_offset = self._alignment_offset
        return Rect(
            raw_rect.x + alignment_offset.x,
            raw_rect.y + alignment_offset.y,
            raw_rect.width,
            raw_rect.height,
        )

    def _render_slice(
        self,
        pos: Point,
        inside_flowable: bool,
        clip_start_x: Optional[Unit] = None,
        clip_width: Optional[Unit] = None,
    ):
        """Render a horizontal slice of a text object.

        Args:
            pos: The doc-space position of the slice beginning
                (at the top-left corner of the slice)
            clip_start_x: The starting local x position in of the slice
            clip_width: The horizontal length of the slice to
                be rendered
            inside_flowable: Whether this is being rendered in a flowable.
                This affects the treatment of the interface position and parent.
        """
        slice_interface = TextInterface(
            pos + self._alignment_offset,
            None if inside_flowable else self.parent.interface_for_children,
            self.scale,
            self.rotation,
            self.transform_origin,
            self.brush.interface,
            self.pen.interface,
            self.text,
            self.font.interface,
            self.background_brush.interface if self.background_brush else None,
            clip_start_x,
            clip_width,
        )
        slice_interface.render()
        self.interfaces.append(slice_interface)

    def render_complete(
        self,
        pos: Point,
        flowable_line: Optional[NewLine] = None,
        flowable_x: Optional[Unit] = None,
    ):
        inside_flowable = bool(flowable_line)
        self._render_slice(pos, inside_flowable, None, None)

    def render_before_break(self, pos: Point, flowable_line: NewLine, flowable_x: Unit):
        slice_length = flowable_line.length - (flowable_x - flowable_line.flowable_x)
        self._render_slice(pos, True, ZERO, slice_length)

    def render_spanning_continuation(
        self, pos: Point, flowable_line: NewLine, object_x: Unit
    ):
        self._render_slice(pos, True, object_x, flowable_line.length)

    def render_after_break(self, pos: Point, flowable_line: NewLine, object_x: Unit):
        self._render_slice(pos, True, object_x, None)
