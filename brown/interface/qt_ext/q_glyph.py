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
        self._bounding_rect = bounding_rect
        self._origin_offset = origin_offset
        super().__init__(*args, **kwargs)

    def boundingRect(self):
        if not self._bounding_rect:
            return super().boundingRect()
        return self._bounding_rect

    def pos(self):
        if not self._origin_offset:
            return super().pos()
        return super.pos() + self._origin_offset
