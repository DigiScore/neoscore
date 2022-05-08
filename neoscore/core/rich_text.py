from __future__ import annotations

from typing import Optional

from neoscore.core import neoscore
from neoscore.core.font import Font
from neoscore.core.layout_controllers import NewLine
from neoscore.core.point import Point, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Unit
from neoscore.interface.rich_text_interface import RichTextInterface


class RichText(PositionedObject):

    """A graphical rich text object.

    Unlike its simpler counterpart in ``Text``, this supports rich
    formatting with HTML input. As neoscore is currently backed by Qt,
    this input supports Qt's HTML subset documented at
    https://doc.qt.io/qt-5/richtext-html-subset.html
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
        html_text: str,
        width: Optional[Unit] = None,
        font: Optional[Font] = None,
        scale: float = 1,
        rotation: float = 0,
        z_index: int = 0,
    ):
        """
        Args:
            pos: Position relative to the parent
            parent: The parent (core-level) object or None
            html_text: The text to be displayed, written in HTML.
            width: The maximum width for the displayed text. If omitted,
                lines will only break when explicitly called for by the HTML.
            font: The default font to display the text in.
            scale: A scaling factor relative to the font size.
            rotation: Rotation angle in degrees.
            z_index: Controls draw order with lower values drawn first.
        """
        if font:
            self._font = font
        else:
            self._font = neoscore.default_font
        self._html_text = html_text
        self._width = width
        self._scale = scale
        self._rotation = rotation
        self._z_index = z_index
        super().__init__(pos, parent)

    @property
    def breakable_length(self) -> Unit:
        """The breakable length of the object.

        This is always 0, meaning RichText objects cannot be broken
        across Flowable lines.
        """
        return ZERO

    @property
    def html_text(self) -> str:
        """The text to be displayed, written in HTML."""
        return self._html_text

    @html_text.setter
    def html_text(self, value: str):
        self._html_text = value

    @property
    def width(self) -> Optional[Unit]:
        """The maximum width for the displayed text.

        If omitted, lines will only break when explicitly called for
        by the HTML.
        """
        return self._width

    @width.setter
    def width(self, value: Optional[Unit]):
        self._width = value

    @property
    def font(self) -> Font:
        """The default font used to display the text.

        HTML markup can override this to different styles and famililes.
        """
        return self._font

    @font.setter
    def font(self, value: Font):
        self._font = value

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
    def z_index(self) -> int:
        """Value controlling draw order with lower values being drawn first"""
        return self._z_index

    @z_index.setter
    def z_index(self, value: int):
        self._z_index = value

    # Since RichText isn't breakable (for now?), we only need to
    # implement complete rendering
    def render_complete(
        self,
        pos: Point,
        flowable_line: Optional[NewLine] = None,
        flowable_x: Optional[Unit] = None,
    ):
        interface = RichTextInterface(
            pos,
            self.html_text,
            self.font.interface,
            self.width,
            self.scale,
            self.rotation,
            self.z_index,
        )
        interface.render()
        self.interfaces.append(interface)
