from PyQt5.QtGui import QBrush, QColor, QPainter, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem

from neoscore.core import env


class QRichTextItem(QGraphicsTextItem):
    """A lighted specialized version of ``QGraphicsTextItem``

    * Enables painter caching
    * Allows debugging bounding rect drawing
    * Enables anti-aliasing
    """

    def __init__(self):
        super().__init__()
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)

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
