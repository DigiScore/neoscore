from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem

from neoscore.core import env
from neoscore.core.point import ORIGIN
from neoscore.interface.qt.converters import point_to_qt_point_f


class QRichTextItem(QGraphicsTextItem):
    """A lighted specialized version of ``QGraphicsTextItem``

    * Enables painter caching
    * Allows debugging bounding rect drawing
    * Enables anti-aliasing
    """

    def __init__(
        self,
        transform_origin: QPointF = ORIGIN,
    ):
        """
        Args:
            transform_origin: The origin point for rotation and scaling transforms
        """
        super().__init__()
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        self.setTransformOriginPoint(point_to_qt_point_f(transform_origin))

    def paint(self, painter: QPainter, *args, **kwargs):
        if env.DEBUG:
            bounding_rect = self.boundingRect()
            painter.setBrush(QBrush())
            painter.setPen(QPen(QColor("#ff0000"), 0))
            painter.drawRect(bounding_rect)
        # Enable text anti-aliasing - for some reason the global render hint isn't
        # applied here.
        painter.setRenderHint(0x02)
        super().paint(painter, *args, **kwargs)
