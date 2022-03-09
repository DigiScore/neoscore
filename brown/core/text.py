from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from brown.core import brown
from brown.core.font import Font
from brown.core.graphic_object import GraphicObject
from brown.core.pen import NO_PEN
from brown.interface.text_interface import TextInterface
from brown.utils.point import Point, PointDef
from brown.utils.units import ZERO, Unit

if TYPE_CHECKING:
    from brown.core.mapping import Parent


# TODO HIGH it's unclear why this `scale` arg is given priority over
# other transforms. I think probably it should be removed so it's not
# confused with font size. Additional scale can be set with grob->qt transforms


class Text(GraphicObject):

    """A graphical text object."""

    def __init__(
        self,
        pos: PointDef,
        text: str,
        font: Optional[Font] = None,
        parent: Optional[Parent] = None,
        scale: float = 1,
    ):
        """
        Args:
            pos: Position relative to the parent
            text: The text to be displayed
            font: The font to display the text in.
            parent: The parent (core-level) object or None
            scale: A hard scaling factor.
        """
        if font:
            self._font = font
        else:
            self._font = brown.default_font
        self._text = text
        self._scale = scale
        super().__init__(pos, parent=parent)

    ######## PUBLIC PROPERTIES ########

    @property
    def text(self):
        """str: The text to be drawn"""
        return self._text

    @property
    def font(self):
        """Font: The text font"""
        return self._font

    @font.setter
    def font(self, value):
        self._font = value

    @property
    def baseline_y(self):
        """Unit: The y coordinate of the first text line's baseline."""
        return self.y + self.font.ascent

    @property
    def scale(self):
        """float: A hard scale factor to be applied to the rendered text"""
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value

    ######## PRIVATE PROPERTIES ########

    @property
    def bounding_rect(self):
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
            NO_PEN.interface,
            self.brush.interface,
            self.text,
            self.font._interface,
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

    def _render_after_break(self, local_start_x: Unit, start: Point, stop: Point):
        self._render_slice(start, local_start_x, stop.x - start.x)

    def _render_spanning_continuation(
        self, local_start_x: Unit, start: Point, stop: Point
    ):
        self._render_slice(start, local_start_x, stop.x - start.x)
