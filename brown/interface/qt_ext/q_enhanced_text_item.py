from PyQt5 import QtWidgets, QtCore


class QEnhancedTextItem(QtWidgets.QGraphicsSimpleTextItem):

    """A text item giving explicit control over positioning and scale.

    This is a modified QGraphicsSimpleTextItem which acts mostly like
    its superclass, with the following extensions:

    * It can be given a rendering offset which forces a painting offset
      indicated by a point vector.
    * It can be given a scaling factor which triggers a hard scale on
      top of its font size.

    Scaling is performed relative to the origin.
    """

    def __init__(self, *args, origin_offset=None, scale_factor=1, **kwargs):
        """
        Args:
            origin_offset(QPointF): The offset of the glyph's origin from (0, 0)
            scale_factor(float): A hard scaling factor.

        All other args are passed directly to QGraphicsSimpleTextItem
        """
        self._origin_offset = origin_offset
        self._scale_factor = scale_factor
        super().__init__(*args, **kwargs)

    def boundingRect(self):
        rect = super().boundingRect()
        rect.translate(self._origin_offset * -1)
        scaled_rect = QtCore.QRectF(rect.x() * self._scale_factor,
                                    rect.y() * self._scale_factor,
                                    rect.width() * self._scale_factor,
                                    rect.height() * self._scale_factor)
        return scaled_rect

    def paint(self, painter, option, widget):
        # For some reason, this seems to need to be scaled *before*
        # translating, while the boundingRect needs to be translated
        # before scaling...
        painter.scale(self._scale_factor, self._scale_factor)
        painter.translate(self._origin_offset * -1)
        super().paint(painter, option, widget)
