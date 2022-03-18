from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core import neoscore
from neoscore.core.brush import SimpleBrushDef
from neoscore.core.font import Font
from neoscore.core.painted_object import PaintedObject
from neoscore.core.pen import NO_PEN, SimplePenDef
from neoscore.interface.text_interface import TextInterface
from neoscore.utils.point import Point, PointDef
from neoscore.utils.rect import Rect
from neoscore.utils.units import ZERO, Unit

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


# TODO HIGH support Pen and Brush for this.
# brush is supported with a post-init setter, pen isn't supported at all.


class Text(PaintedObject):

    """A graphical text object."""

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[Parent],
        text: str,
        # TODO HIGH how to order these args? in MusicPaths, font comes
        # after brush and pen, but here it feels more natural for font
        # to come first since it has such an effect on the
        # shape. maybe update musicpaths signatures?
        font: Optional[Font] = None,
        brush: Optional[SimpleBrushDef] = None,
        pen: Optional[SimplePenDef] = None,
        scale: float = 1,
        breakable: bool = True,
    ):
        """
        Args:
            pos: Position relative to the parent
            parent: The parent (core-level) object or None
            text: The text to be displayed
            brush: The brush to fill in text shapes with.
            pen: The pen to trace text outlines with. This defaults to no pen.
            font: The font to display the text in.
            scale: A scaling factor relative to the font size.
            breakable: Whether this object should break across lines in
                Flowable containers.
        """
        if font:
            self._font = font
        else:
            self._font = neoscore.default_font
        self._text = text
        self._scale = scale
        self._breakable = breakable
        super().__init__(pos, parent, brush, pen or NO_PEN)

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self) -> Unit:
        """The breakable width of the object.

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
    def breakable(self) -> bool:
        """Whether this object should be broken across flowable lines."""
        return self._breakable

    @breakable.setter
    def breakable(self, value: bool):
        self._breakable = value

    ######## PRIVATE PROPERTIES ########

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
