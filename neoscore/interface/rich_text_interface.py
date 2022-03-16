from dataclasses import dataclass
from typing import Optional

from PyQt5.QtWidgets import QGraphicsTextItem

from neoscore.core import neoscore
from neoscore.interface.font_interface import FontInterface
from neoscore.interface.graphic_object_interface import GraphicObjectInterface
from neoscore.interface.qt.converters import point_to_qt_point_f
from neoscore.utils.units import Unit

# TODO HIGH seems like these dont use brush and pen, so maybe brush
# and pen shouldn't be members of grob interface


@dataclass(frozen=True)
class RichTextInterface(GraphicObjectInterface):

    """An interface for graphical text objects."""

    html_text: str

    font: FontInterface

    width: Optional[Unit]

    scale: float = 1

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the line to the scene."""
        print("rendering")
        qt_object = self._create_qt_object()
        neoscore._app_interface.scene.addItem(qt_object)

    def _create_qt_object(self) -> QGraphicsTextItem:
        """Create and return this interface's underlying Qt object"""
        qt_object = QGraphicsTextItem()
        qt_object.setHtml(self.html_text)
        qt_object.setPos(point_to_qt_point_f(self.pos))
        qt_object.setTextWidth(self.width.base_value if self.width is not None else -1)
        qt_object.setFont(self.font.qt_object)
        return qt_object
