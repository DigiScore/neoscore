from typing import Optional

from PyQt5 import QtCore
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QBrush, QColor, QPainterPath, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem

from neoscore.constants import DEBUG


class QClippingPath(QGraphicsPathItem):

    """A QGraphicsPathItem extension supporting horizontal path clipping.

    Works like a `QGraphicsPathItem` except that it renders a
    horizontal slice of the path. Clipping occurs independently of
    scaling.

    While the Qt superclass is mutable, this is intended to be treated
    immutably. Mutations after instantation will result unexpected
    behavior. Object mutations at higher abstraction levels should
    result in new Qt objects created.
    """

    def __init__(
        self,
        qt_path: QPainterPath,
        clip_start_x: Optional[float],
        clip_width: Optional[float],
        scale: float = 1,
    ):
        """
        Args:
            qt_path: The path for the item. This value should
                be the same as in `QGraphicsPathItem.__init__()`
            clip_start_x: The local starting position for the path clipping region.
                This should not adjust for scaling, as that is performed
                automatically. Use `None` to render from the start.
            clip_width: The width of the path clipping region. This should not adjust
                for scaling, as that is performed automatically. Use `None` to render
                to the end
            scale: A scaling factor on the object's coordinate system.
        """
        super().__init__(qt_path)
        super().setScale(scale)
        self.clip_start_x = None if clip_start_x is None else clip_start_x / scale
        self.clip_width = None if clip_width is None else clip_width / scale
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        self.padding = self.pen().width() / scale
        self.update_geometry()

    def boundingRect(self):
        return self.bounding_rect

    def paint(self, painter, *args, **kwargs):
        """Paint with automatic clipping.

        This is overridden from `QGraphicsPathItem.paint()`
        """
        if self.painter_offset:
            painter.translate(self.painter_offset)
        painter.setClipRect(self.clip_rect)
        super().paint(painter, *args, **kwargs)
        if DEBUG:
            painter.setBrush(QBrush())
            painter.setPen(QPen(QColor("#ff0000")))
            painter.drawRect(self.bounding_rect)

    def update_geometry(self):
        self.prepareGeometryChange()
        path_bounding_rect = self.path().boundingRect()
        self.clip_rect = QClippingPath.calculate_clipping_area(
            path_bounding_rect,
            self.clip_start_x,
            self.clip_width,
            self.padding,
        )
        self.bounding_rect = QClippingPath.calculate_bounding_rect(
            path_bounding_rect,
            self.clip_start_x,
            self.clip_width,
            self.padding,
        )
        if self.clip_start_x is not None:
            self.painter_offset = QtCore.QPointF(-1 * self.clip_start_x, 0)
        else:
            self.painter_offset = None

    @staticmethod
    def calculate_clipping_area(
        bounding_rect: QRectF,
        clip_start_x: Optional[float],
        clip_width: Optional[float],
        padding: float,
    ) -> QRectF:
        """Create a QRectF giving the painting area for the object.

        Args:
            bounding_rect: The full shape's bounding rectangle
            clip_start_x: The local starting position for the
                clipping region. Use `None` to render from the start.
            clip_width: The width of the clipping region.
                Use `None` to render to the end
            padding: Extra area padding to be added to all sides of the
                clipping area. This might be useful, for instance,
                for making sure thick pen strokes render completely.
        """
        resolved_clip_start_x = (
            clip_start_x if clip_start_x is not None else bounding_rect.x()
        )
        resolved_clip_width = (
            clip_width
            if clip_width is not None
            else bounding_rect.width() - (resolved_clip_start_x - bounding_rect.x())
        )
        return QtCore.QRectF(
            resolved_clip_start_x - padding,
            bounding_rect.y() - padding,
            resolved_clip_width + (padding * 2),
            bounding_rect.height() + (padding * 2),
        )

    @staticmethod
    def calculate_bounding_rect(
        bounding_rect: QRectF,
        clip_start_x: Optional[float],
        clip_width: Optional[float],
        padding: float,
    ) -> QRectF:
        """Create a QRectF giving the bounding rect for the path.

        Args:
            bounding_rect: The full shape's bounding rectangle
            clip_start_x: The local starting position for the
                clipping region. Use `None` to render from the start.
            clip_width: The width of the clipping region.
                Use `None` to render to the end
            padding: Extra area padding to be added to all sides of the clipping area.
                This might be useful, for instance, for making sure thick pen strokes
                render completely.
        """
        resolved_clip_start_x = (
            clip_start_x if clip_start_x is not None else bounding_rect.x()
        )
        resolved_clip_width = (
            clip_width
            if clip_width is not None
            else bounding_rect.width() - resolved_clip_start_x
        )
        return QRectF(
            -padding,
            bounding_rect.y() - padding,
            resolved_clip_width + (padding * 2),
            bounding_rect.height() + (padding * 2),
        )
