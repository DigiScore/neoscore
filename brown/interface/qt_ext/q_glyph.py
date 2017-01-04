from PyQt5 import QtWidgets


class QGlyph(QtWidgets.QGraphicsSimpleTextItem):

    """A glyph giving explicit control over coordinate handling"""

    def __init__(self, *args, bounding_rect=None, origin_offset=None, **kwargs):
        """
        Args:
            bounding_rect(QRectF): The explicit bounding rect for the glyph
            origin_offset(QPointF): The offset of the glyph's origin from (0, 0)

        All other args are passed directly to QGraphicsSimpleTextItem
        """
        # TODO: Remove defunct bounding rect passing logic
        self._bounding_rect = bounding_rect
        self._origin_offset = origin_offset
        super().__init__(*args, **kwargs)

    def boundingRect(self):
        rect = super().boundingRect()
        rect.translate(self._origin_offset * -1)
        return rect

    def paint(self, painter, option, widget):
        # print('origin offset: {}'.format(self._origin_offset))
        painter.translate(self._origin_offset * -1)
        super().paint(painter, option, widget)
