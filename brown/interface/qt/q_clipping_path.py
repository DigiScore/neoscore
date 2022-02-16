from typing import Optional

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainterPath

from brown.utils.units import GraphicUnit, Unit


class QClippingPath(QtWidgets.QGraphicsPathItem):

    """A QGraphicsPathItem extension supporting horizontal path clipping.

    Works like a `QGraphicsPathItem` except that it renders a
    horizontal slice of the path. Clipping occurs independently of
    scaling.

    """

    def __init__(
        self,
        qt_path: QPainterPath,
        clip_start_x: Optional[Unit],
        clip_width: Optional[Unit],
        scale: float = 1,
    ):
        """
        Args:
            qt_path (QPainterPath): The path for the item. This value should
                be the same as in `QGraphicsPathItem.__init__()`
            clip_start_x (Unit or None): The local starting position for the
                path clipping region. Use `None` to render from the start.
            clip_width (Unit or None): The width of the path clipping region.
                Use `None` to render to the end
            scale (float): An initial Qt scale factor.
        """
        super().__init__(qt_path)
        self.setScale(scale)
        self.clip_start_x = clip_start_x
        self.clip_width = clip_width
        self.update_geometry()

    def boundingRect(self):
        return self.bounding_rect

    def paint(self, painter, *args, **kwargs):
        """Paint with automatic clipping.

        This is overridden from `QGraphicsPathItem.paint()`
        """
        painter.save()
        if self.painter_offset:
            painter.translate(self.painter_offset)
        painter.setClipRect(self.clip_rect)
        super().paint(painter, *args, **kwargs)
        painter.restore()

    def update_geometry(self):
        self.clip_rect = QClippingPath.calculate_clipping_area(
            self.path().boundingRect(),
            self.clip_start_x,
            self.clip_width,
            self.pen().width(),
            self.scale(),
        )
        self.bounding_rect = QClippingPath.calculate_bounding_rect(
            self.path().boundingRect(),
            self.clip_start_x,
            self.clip_width,
            self.pen().width(),
            self.scale(),
        )
        if self.clip_start_x is not None:
            self.painter_offset = QtCore.QPointF(
                (-1 * self.scale() * GraphicUnit(self.clip_start_x).value)
                / self.scale(),
                0,
            )
        else:
            self.painter_offset = None
        self.prepareGeometryChange()

    @staticmethod
    def calculate_clipping_area(
        bounding_rect, clip_start_x, clip_width, extra_padding, scale
    ):
        """Create a QRectF giving the painting area for the object.

        Args:
            bounding_rect (QRectF): The full shape's bounding rectangle
            clip_start_x (Unit or None): The local starting position for the
                clipping region. Use `None` to render from the start.
            clip_width (Unit or None): The width of the clipping region.
                Use `None` to render to the end
            extra_padding (float): Extra area padding to be added to all
                sides of the clipping area. This might be useful, for instance,
                for making sure thick pen strokes render completely.

        Returns: QRectF
        """
        clip_start_x = (
            bounding_rect.x()
            if clip_start_x is None
            else GraphicUnit(clip_start_x).value
        )
        clip_width = (
            bounding_rect.width() - (clip_start_x - bounding_rect.x())
            if clip_width is None
            else GraphicUnit(clip_width).value
        )
        padding = GraphicUnit(extra_padding).value
        return QtCore.QRectF(
            (clip_start_x - padding) / scale,
            (bounding_rect.y() - padding) / scale,
            (clip_width + (padding * 2)) / scale,
            (bounding_rect.height() + (padding * 2)) / scale,
        )

    @staticmethod
    def calculate_bounding_rect(
        bounding_rect, clip_start_x, clip_width, extra_padding, scale
    ):
        """Create a QRectF giving the bounding rect for the path.

        Args:
            bounding_rect (QRectF): The full shape's bounding rectangle
            clip_start_x (Unit or None): The local starting position for the
                clipping region. Use `None` to render from the start.
            clip_width (Unit or None): The width of the clipping region.
                Use `None` to render to the end
            extra_padding (float): Extra area padding to be added to all
                sides of the clipping area. This might be useful, for instance,
                for making sure thick pen strokes render completely.

        Returns: QRectF
        """
        clip_start_x = (
            bounding_rect.x()
            if clip_start_x is None
            else GraphicUnit(clip_start_x).value
        )
        clip_width = (
            bounding_rect.width() - clip_start_x
            if clip_width is None
            else GraphicUnit(clip_width).value
        )
        padding = GraphicUnit(extra_padding).value
        return QtCore.QRectF(
            (-padding) / scale,
            (-padding) / scale,
            (clip_width + (padding * 2)) / scale,
            (bounding_rect.height() + (padding * 2)) / scale,
        )
