from dataclasses import dataclass
from typing import Optional

from neoscore.core.units import Unit
from neoscore.interface.font_interface import FontInterface
from neoscore.interface.positioned_object_interface import PositionedObjectInterface
from neoscore.interface.qt.converters import point_to_qt_point_f
from neoscore.interface.qt.q_rich_text_item import QRichTextItem


@dataclass(frozen=True)
class RichTextInterface(PositionedObjectInterface):

    """An interface for graphical text objects."""

    html_text: str

    font: FontInterface

    width: Optional[Unit] = None

    def render(self):
        """Render the line to the scene."""
        self._register_qt_object(self._create_qt_object())

    def _create_qt_object(self) -> QRichTextItem:
        """Create and return this interface's underlying Qt object"""
        qt_object = QRichTextItem()
        qt_object.setHtml(self.html_text)
        qt_object.document().setDocumentMargin(0)
        qt_object.setPos(point_to_qt_point_f(self.pos))
        qt_object.setTextWidth(self.width.base_value if self.width is not None else -1)
        qt_object.setFont(self.font.qt_object)
        qt_object.setTransformOriginPoint(point_to_qt_point_f(self.transform_origin))
        if self.scale != 1:
            qt_object.setScale(self.scale)
        if self.rotation != 0:
            qt_object.setRotation(self.rotation)
        return qt_object
