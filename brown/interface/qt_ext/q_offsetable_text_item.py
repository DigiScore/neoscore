from PyQt5 import QtWidgets


class QOffsetableTextItem(QtWidgets.QGraphicsSimpleTextItem):

    """A text item giving explicit control over coordinate handling

    This is a modified QGraphicsSimpleTextItem which acts mostly like
    its superclass, with the exception that it can be given a rendering
    offset which forces a painting offset indicated by a point vector.
    """

    def __init__(self, *args, origin_offset=None, **kwargs):
        """
        Args:
            origin_offset(QPointF): The offset of the glyph's origin from (0, 0)

        All other args are passed directly to QGraphicsSimpleTextItem
        """
        self._origin_offset = origin_offset
        super().__init__(*args, **kwargs)

    def boundingRect(self):
        rect = super().boundingRect()
        rect.translate(self._origin_offset * -1)
        return rect

    def paint(self, painter, option, widget):
        painter.translate(self._origin_offset * -1)
        super().paint(painter, option, widget)
