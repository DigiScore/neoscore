from dataclasses import dataclass

from PyQt5.QtWidgets import QGraphicsSimpleTextItem

from neoscore.core.point import ORIGIN
from neoscore.interface.positioned_object_interface import PositionedObjectInterface
from neoscore.interface.qt.converters import point_to_qt_point_f


@dataclass(frozen=True)
class InvisibleObjectInterface(PositionedObjectInterface):
    """A stub interface for use as a virtual parent in scenes."""

    def render(self):
        qt_object = QGraphicsSimpleTextItem()
        qt_object.setPos(point_to_qt_point_f(self.pos))
        if self.transform_origin != ORIGIN:
            qt_object.setTransformOriginPoint(
                point_to_qt_point_f(self.transform_origin)
            )
        if self.scale != 1:
            qt_object.setScale(self.scale)
        if self.rotation != 0:
            qt_object.setRotation(self.rotation)
        if self.transform_origin != ORIGIN:
            qt_object.setTransformOriginPoint(
                point_to_qt_point_f(self.transform_origin)
            )
        self._register_qt_object(qt_object)
