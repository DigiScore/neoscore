from PyQt5 import QtCore, QtWidgets

from brown.interface.qt.converters import unit_to_qt_float
from brown.interface.qt.q_clipping_path import QClippingPath

""" NOTE: I think the origin offset stuff is only needed because QT's
QGraphicsSimpleTextItem sets its original from the top left corner of
text, and we need to position them from their baseline. By using raw
paths for all text items, then using QPainterPath.addText --- which
positions from baseline --- I think we can avoid this complication
entirely.  """


class QEnhancedTextItem(QtWidgets.QGraphicsSimpleTextItem):

    """A text item giving explicit control over positioning and scale.

    This is a modified QGraphicsSimpleTextItem which acts mostly like
    its superclass, with the following extensions:

    * It can be given a rendering offset which forces a painting offset
      indicated by a point vector.
    * It can be given a scaling factor which triggers a hard scale on
      top of its font size. Scaling is performed relative to the origin.
    * It can be clipped to render any horizontal slice of its image.
    """

    def __init__(
        self,
        *args,
        origin_offset=None,
        scale=1,
        clip_start_x=None,
        clip_width=None,
        **kwargs
    ):
        """
        Args:
            origin_offset (QPointF): The offset of the glyph's origin from (0, 0)
            scale (float): A hard scaling factor.
            clip_start_x (Unit or None): The local starting position for the
                clipping region. Use `None` to render from the start.
            clip_width (Unit or None): The width of the clipping region.
                Use `None` to render to the end

        All other args are passed directly to QGraphicsSimpleTextItem
        """
        super().__init__(*args, **kwargs)
        self.origin_offset = origin_offset
        self.scale = scale
        self.clip_start_x = clip_start_x
        self.clip_width = clip_width
        self.update_geometry()

    def calculate_bounding_rect(self):
        rect = super().boundingRect()
        rect.translate(self.origin_offset * -1)
        scaled_rect = QtCore.QRectF(
            rect.x() * self.scale,
            rect.y() * self.scale,
            rect.width() * self.scale,
            rect.height() * self.scale,
        )
        return scaled_rect

    def calculate_clip_rect(self):
        # Get clip area in logical (not scaled or offset) space
        return QClippingPath.calculate_clipping_area(
            super().boundingRect(),
            (self.clip_start_x if self.clip_start_x is not None else None),
            (self.clip_width if self.clip_width is not None else None),
            self.pen().width(),
            self.scale,
        )

    def calculate_clip_offset(self):
        if self.clip_start_x is not None:
            main_offset = QtCore.QPointF(
                -1 * unit_to_qt_float(self.clip_start_x / self.scale), 0
            )
        else:
            main_offset = QtCore.QPointF(0, 0)
        return (self.origin_offset * -1) + main_offset

    def update_geometry(self):
        self.bounding_rect = self.calculate_bounding_rect()
        self.painter_offset = self.calculate_clip_offset()
        self.clip_rect = self.calculate_clip_rect()
        self.prepareGeometryChange()

    def boundingRect(self):
        return self.bounding_rect

    def paint(self, painter, option, widget):
        # For some reason, this seems to need to be scaled *before*
        # translating, while the boundingRect needs to be translated
        # before scaling...
        painter.save()
        painter.scale(self.scale, self.scale_factor)
        painter.translate(self.painter_offset)
        painter.setClipRect(self.clip_rect)
        super().paint(painter, option, widget)
        painter.restore()
