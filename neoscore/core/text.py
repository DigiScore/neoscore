from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core import neoscore
from neoscore.core.brush import Brush, BrushDef
from neoscore.core.font import Font
from neoscore.core.painted_object import PaintedObject
from neoscore.core.pen import Pen, PenDef
from neoscore.core.point import Point, PointDef
from neoscore.core.rect import Rect
from neoscore.core.units import ZERO, Unit
from neoscore.interface.text_interface import TextInterface

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class Text(PaintedObject):

    """A graphical text object."""

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[Parent],
        text: str,
        font: Optional[Font] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
        scale: float = 1,
        rotation: float = 0,
        background_brush: Optional[BrushDef] = None,
        z_index: int = 0,
        breakable: bool = True,
    ):
        """
        Args:
            pos: Position relative to the parent
            parent: The parent (core-level) object or None
            text: The text to be displayed
            font: The font to display the text in.
            brush: The brush to fill in text shapes with.
            pen: The pen to trace text outlines with. This defaults to no pen.
            scale: A scaling factor relative to the font size.
            rotation: Angle in degrees. Note that breakable rotated text is
                not currently supported.
            background_brush: Optional brush used to paint the text's bounding rect
                behind it.
            z_index: Controls draw order with higher values drawn first.
            breakable: Whether this object should break across lines in
                Flowable containers.
        """
        if font:
            self._font = font
        else:
            self._font = neoscore.default_font
        self._text = text
        self._scale = scale
        self._rotation = rotation
        self.background_brush = background_brush
        self._z_index = z_index
        self._breakable = breakable
        super().__init__(pos, parent, brush, pen or Pen.no_pen())

    ######## PUBLIC PROPERTIES ########

    @property
    def breakable_length(self) -> Unit:
        """The breakable length of the object.

        This is used to determine how and where rendering cuts should be made.

        This is derived from other properties and cannot be set directly.
        """
        if self.breakable:
            return self.bounding_rect.width
        else:
            return ZERO

    @property
    def text(self) -> str:
        """The text to be drawn"""
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

    @property
    def font(self) -> Font:
        """The text font"""
        return self._font

    @font.setter
    def font(self, value: Font):
        self._font = value

    @property
    def baseline_y(self) -> Unit:
        """The y coordinate of the first text line's baseline."""
        return self.y + self.font.ascent

    @property
    def scale(self) -> float:
        """A scale factor to be applied to the rendered text"""
        return self._scale

    @scale.setter
    def scale(self, value: float):
        self._scale = value

    @property
    def rotation(self) -> float:
        """An angle in degrees to rotate about the text origin"""
        return self._rotation

    @rotation.setter
    def rotation(self, value: float):
        self._rotation = value

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
    def z_index(self) -> int:
        """Value controlling draw order with higher values being drawn first"""
        return self._z_index

    @z_index.setter
    def z_index(self, value: int):
        self._z_index = value

    @property
    def breakable(self) -> bool:
        """Whether this object should be broken across flowable lines."""
        return self._breakable

    @breakable.setter
    def breakable(self, value: bool):
        self._breakable = value

    @property
    def bounding_rect(self) -> Rect:
        """The bounding rect override for this text."""
        return self.font.bounding_rect_of(self.text)

    ######## PRIVATE METHODS ########

    def _render_slice(
        self,
        pos: Point,
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
        """
        slice_interface = TextInterface(
            pos,
            self.brush.interface,
            self.pen.interface,
            self.text,
            self.font.interface,
            self.scale,
            self.rotation,
            self.background_brush.interface if self.background_brush else None,
            self.z_index,
            clip_start_x,
            clip_width,
        )
        slice_interface.render()
        self.interfaces.append(slice_interface)

    def _render_complete(
        self,
        pos: Point,
        dist_to_line_start: Optional[Unit] = None,
        local_start_x: Optional[Unit] = None,
    ):
        self._render_slice(pos, None, None)

    def _render_before_break(
        self, local_start_x: Unit, start: Point, stop: Point, dist_to_line_start: Unit
    ):
        self._render_slice(start, ZERO, stop.x - start.x)

    def _render_after_break(self, local_start_x: Unit, start: Point):
        self._render_slice(start, local_start_x, None)

    def _render_spanning_continuation(
        self, local_start_x: Unit, start: Point, stop: Point
    ):
        self._render_slice(start, local_start_x, stop.x - start.x)
