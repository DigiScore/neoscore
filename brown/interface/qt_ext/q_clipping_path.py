from PyQt5 import QtCore, QtWidgets

from brown.utils.units import GraphicUnit


class QClippingPath(QtWidgets.QGraphicsPathItem):

    """A QGraphicsPathItem extension supporting horizontal path clipping.

    Works exactly like a `QGraphicsPathItem` except that it renders a
    horizontal slice of the path.
    """

    def __init__(self, qt_path, clip_start_x, clip_width):
        """
        Args:
            qt_path (QPainterPath): The path for the item. This value should
                be the same as in `QGraphicsPathItem.__init__()`
            clip_start_x (Unit or None): The local starting position for the
                path clipping region. Use `None` to render from the start.
            clip_width (Unit or None): The width of the path clipping region.
                Use `None` to render to the end
        """
        self.clip_start_x = clip_start_x
        self.clip_width = clip_width
        super().__init__(qt_path)

    def paint(self, painter, *args, **kwargs):
        """Paint, clipping by `self._clip_area`.

        This is an overload of `QGraphicsPathItem.paint()`"""
        painter.save()
        if self.clip_start_x is not None:
            painter.translate(QtCore.QPointF(
                -1 * float(GraphicUnit(self.clip_start_x)), 0))
        clip_area = self.create_clipping_area(
            self.path().boundingRect(),
            self.clip_start_x,
            self.clip_width,
            self.pen().width())
        painter.setClipRect(clip_area)
        super().paint(painter, *args, **kwargs)
        painter.restore()

    @staticmethod
    def create_clipping_area(bounding_rect,
                             clip_start_x,
                             clip_width,
                             extra_padding):
        """Create a QRectF giving the painting area for the object.

        Args:
            bounding_rect (QRectF): The full shape's bounding rectangle
            clip_start_x (Unit or None): The local starting position for the
                clipping region. Use `None` to render from the start.
            width (Unit or None): The width of the clipping region.
                Use `None` to render to the end
            extra_padding (float): Extra area padding to be added to all
                sides of the clipping area. This might be useful, for instance,
                for making sure thick pen strokes render completely.

        Returns: QRectF
        """
        if clip_start_x is None:
            clip_start_x = bounding_rect.x()
        else:
            clip_start_x = float(GraphicUnit(clip_start_x))
        if clip_width is None:
            clip_width = bounding_rect.width() - clip_start_x
        else:
            clip_width = float(GraphicUnit(clip_width))
        padding = float(GraphicUnit(extra_padding))
        return QtCore.QRectF(clip_start_x - padding,
                             bounding_rect.y() - padding,
                             clip_width + (padding * 2),
                             bounding_rect.height() + (padding * 2))
