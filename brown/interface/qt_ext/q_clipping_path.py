from PyQt5 import QtCore, QtWidgets, QtGui

from brown.utils.units import Unit


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
        self.clip_start_x = start_x
        self.clip_width = width
        super().__init__(qt_path)

    def paint(self, painter, *args, **kwargs):
        """Paint, clipping by `self._clip_area`.

        This is an overload of `QGraphicsPathItem.paint()`"""
        if self.clip_start_x is not None:
            painter.translate(QtCore.QPointF(
                -1 * float(Unit(self.clip_start_x)), 0))
        clip_area = self._create_clipping_area(
            self.path(), self.clip_start_x, self.clip_width)
        painter.setClipRect(clip_area)
        super().paint(painter, *args, **kwargs)

    ######## PRIVATE METHODS ########

    def _create_clipping_area(self, painter_path, start_x, clip_width):
        """Create a QPainterPath indicating the area of the path to draw

        Args:
            painter_path (QPainterPath): The reference path.
                This is used to determine the path bounding box.
            start_x (Unit or None): The local starting position for the
                path clipping region.
                Use `None` to render from the start
            width (Unit or None): The width of the path clipping region.
                Use `None` to render to the end

        Returns: QRectF
        """
        bounding_rect = painter_path.boundingRect()
        if start_x is None:
            start_x = bounding_rect.x()
        else:
            start_x = float(Unit(start_x))
        if clip_width is None:
            clip_width = bounding_rect.width() - start_x
        else:
            clip_width = float(Unit(clip_width))
        pen_padding = self.pen().width()
        return QtCore.QRectF(start_x - pen_padding,
                             bounding_rect.y() - pen_padding,
                             clip_width + pen_padding,
                             bounding_rect.height() + pen_padding)
