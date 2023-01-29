from typing import Optional

from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem

from neoscore.core import env


class QClippingPath(QGraphicsPathItem):

    """A QGraphicsPathItem extension supporting horizontal path clipping.

    Works like a ``QGraphicsPathItem`` except that it renders a
    horizontal slice of the path. Rather than rendering the entire
    path, renders the region starting at a given ``clip_start_x`` and
    extending for a given ``clip_width``. This rendered region is
    shifted leftward, so it appears at the path's root position. This
    is useful for splitting a path into horizontal chunks and
    rendering them in different positions, for instance when drawing a
    staff which appears on multiple lines.

    ``clip_start_x`` and ``clip_width`` should not take into account
    scaling. For example if a rendered region of 50 points is required
    on a path with a scale of 2, ``clip_width=50`` should be passed.

    While the Qt superclass is mutable, this is intended to be treated
    immutably. Mutations after instantation will result unexpected
    behavior. Object mutations at higher abstraction levels should
    result in new Qt objects created.

    Internally, the clipping implementation is rather subtle in how it
    integrates with Qt's coordinate and painter systems. The item's
    bounding rect is adjusted to match the requested clip region. At
    render time, the painter translates its coordinate system leftward
    by the (internally scale-adjusted) ``clip_start_x``. The painter's
    clip rect is then derived from the item's bounding rect, but
    shifted rightward to cancel out the painter's translation. These
    actions are all automatically scaled as necessary, since the scale
    is applied to the QClippingPath, not the painter.

    Note that clipping behavior does not play well with rotated items,
    and no API guarantees are currently given about it.
    """

    def __init__(
        self,
        qt_path: QPainterPath,
        clip_start_x: float = 0,
        clip_width: Optional[float] = None,
        scale: float = 1,
        rotation: float = 0,
        background_brush: Optional[QBrush] = None,
        defer_geometry_calculation: bool = False,
        transform_origin: Optional[QPointF] = None,
    ):
        """
        Args:
            qt_path: The path for the item. This value should
                be the same as in ``QGraphicsPathItem.__init__()``
            clip_start_x: The local starting position for the path clipping region.
                This should not adjust for scaling, as that is performed
                automatically. Use ``0`` to render from the start.
            clip_width: The width of the path clipping region. This should not adjust
                for scaling, as that is performed automatically. Use ``None`` to render
                to the end
            scale: A scaling factor on the object's coordinate system.
            rotation: Rotation about the path's origin given in degrees. Rotated path
                clipping is currently not supported.
            background_brush: If given, this will be used to paint over the path's
                bounding rect behind the path.
            defer_geometry_calculation: If true, this constructor will not automatically
                calculate the path's bounding and clipping geometry. When this is set,
                you *must* call ``update_geometry`` when the geometry is finalized.
                This is useful when post-init modifications immediately alter the geometry,
                preventing a redundant calculation.
            transform_origin: The origin point for rotation and scaling transforms
        """
        super().__init__(qt_path)
        self.clip_start_x = clip_start_x / scale
        self.clip_width = None if clip_width is None else clip_width / scale
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        if transform_origin:
            self.setTransformOriginPoint(transform_origin)
        self.setRotation(rotation)
        super().setScale(scale)
        self.background_brush = background_brush
        self.bounding_rect = None
        self.clip_rect = None
        if not defer_geometry_calculation:
            self.update_geometry()

    def boundingRect(self):
        # Seems like this is in logical space (pre-scaling)
        return self.bounding_rect

    def paint(self, painter: QPainter, *args, **kwargs):
        """Paint with automatic clipping.

        This is overridden from ``QGraphicsPathItem.paint()``
        """
        if self.clip_start_x != 0:
            painter.translate(-self.clip_start_x, 0)
        if self.clip_rect is not None:
            painter.setClipRect(self.clip_rect)
        if env.DEBUG or self.background_brush:
            bounding_rect = self.bounding_rect
            if self.clip_start_x != 0:
                # Since painter is translated, cancel that out when
                # drawing the bounding rect
                bounding_rect = bounding_rect.translated(self.clip_start_x, 0)
        if self.background_brush:
            painter.setBrush(self.background_brush)
            painter.setPen(QPen(0))
            painter.drawRect(bounding_rect)
        if env.DEBUG:
            painter.setBrush(QBrush())
            painter.setPen(QPen(QColor("#ff0000"), 0))
            painter.drawRect(bounding_rect)

        super().paint(painter, *args, **kwargs)

    def update_geometry(self):
        """Recalculate the object's bounding and clipping rects.

        This *must* be called after any changes affecting these rects, including pen
        thickness changes.
        """
        self.prepareGeometryChange()
        path_bounding_rect = self.path().boundingRect()
        padding = self.pen().widthF() / 2
        self.bounding_rect = QClippingPath.calculate_bounding_rect(
            path_bounding_rect,
            self.clip_start_x,
            self.clip_width,
            padding,
        )
        # Clip rect is used by painter, which translates by -clip_start_x,
        # so we need to cancel that out here
        self.clip_rect = self.bounding_rect.translated(self.clip_start_x, 0)

    @staticmethod
    def calculate_bounding_rect(
        bounding_rect: QRectF,
        clip_start_x: float,
        clip_width: Optional[float],
        padding: float,
    ) -> QRectF:
        """Create a QRectF giving the bounding rect for the path.

        Args:
            bounding_rect: The full shape's bounding rectangle
            clip_start_x: The local starting position for the
                clipping region. Use ``None`` to render from the start.
            clip_width: The width of the clipping region.
                Use ``None`` to render to the end
            padding: Extra area padding to be added to all non-clipped sides
                of the rect.
        """
        # We used to do this in a more DRY way, but it was very difficult to reason
        # about which factors applied to which cases, so to make things much easier to
        # reason about we simply split each of the 4 cases apart and handle them
        # separately.
        if not clip_start_x and not clip_width:
            # Full bounding rect
            # (Either not in a flowable, or fits completely in line)
            return QRectF(
                bounding_rect.x() - padding,
                bounding_rect.y() - padding,
                bounding_rect.width() + (padding * 2),
                bounding_rect.height() + (padding * 2),
            )
        elif clip_width and (not clip_start_x):
            # Starting from beginning, using a clip width
            # (Incomplete first line in flowable)
            return QRectF(
                bounding_rect.x() - padding,
                bounding_rect.y() - padding,
                # Do not pad right edge
                (clip_width - bounding_rect.x()) + padding,
                bounding_rect.height() + (padding * 2),
            )
        elif clip_width and clip_start_x:
            # Starting from middle of path, using a clip width
            # (After first line in a flowable, but not at the end yet)
            return QRectF(
                # Do not pad left or right edge
                0.0,
                bounding_rect.y() - padding,
                clip_width,
                bounding_rect.height() + (padding * 2),
            )
        elif (not clip_width) and clip_start_x:
            # Starting from middle of path, extends to the end
            # (Last line in flowable after a continuation)
            return QRectF(
                # Do not pad left edge
                0.0,
                bounding_rect.y() - padding,
                (bounding_rect.width() - clip_start_x + bounding_rect.x()) + padding,
                bounding_rect.height() + (padding * 2),
            )
        else:
            raise RuntimeError("Unreachable")
