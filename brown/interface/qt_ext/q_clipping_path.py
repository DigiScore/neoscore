from PyQt5 import QtCore, QtWidgets, QtGui


class QClippingPath(QtWidgets.QGraphicsPathItem):

    """A QGraphicsPathItem extension supporting horizontal path clipping.

    Works exactly like a `QGraphicsPathItem` except that it renders a
    horizontal slice of the path.
    """

    def __init__(self, qt_path, start_x, width):
        """
        Args:
            qt_path (QPainterPath): The path for the item. This value should
                be the same as in `QGraphicsPathItem.__init__()`
            start_x (Unit or None): The local starting position for the
                path clipping region.
                Use `None` to render from the start
            width (Unit or None): The width of the path clipping region.
                Use `None` to render to the end
        """
        bounding_rect = qt_path.boundingRect()
        adjusted_start_x = (bounding_rect.x() if start_x is None
                            else float(start_x))
        adjusted_width = (bounding_rect.width() if width is None
                          else float(width))
        self._clip_area = QtGui.QPainterPaplth()
        self._clip_area.addRect(
            QtCore.QRectF(adjusted_start_x, bounding_rect.y(),
                          adjusted_width, bounding_rect.height()))
        super().__init__(qt_path)

    def paint(self, painter, *args, **kwargs):
        """Paint, clipping by `self._clip_area`.

        This is an overload of `QGraphicsPathItem.paint()`"""
        painter.setClipPath(self._clip_area)
        super().paint(painter, *args, **kwargs)
