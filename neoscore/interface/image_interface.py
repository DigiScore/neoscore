import pathlib
from dataclasses import dataclass

from PyQt5.QtGui import QPixmap
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem

from neoscore.core.exceptions import ImageLoadingError
from neoscore.core.point import ORIGIN
from neoscore.interface.positioned_object_interface import PositionedObjectInterface
from neoscore.interface.qt.converters import point_to_qt_point_f

# Qt::SmoothTransformation
_QT_SMOOTH_TRANSFORMATION = 1


@dataclass(frozen=True)
class ImageInterface(PositionedObjectInterface):

    """Interface for images, including both pixmaps and SVGs.

    Supported image extensions/formats include: BMP, GIF, JPG, JPEG,
    PNG, PBM, PGM, PPM, XBM, XPM, and SVG.

    Scaling respects the image's aspect ratio, and is performed using
    bilinear filtering.
    """

    file_path: pathlib.Path
    """Path to an image file to be used"""

    opacity: float = 1
    """The image's opacity, where 1 is fully opaque and 0 is invisible."""

    @property
    def _resolved_path(self) -> str:
        return str(self.file_path.expanduser())

    def _create_svg_qt_object(self) -> QGraphicsSvgItem:
        qt_object = QGraphicsSvgItem(self._resolved_path)
        self._apply_common_properties(qt_object)
        return qt_object

    def _create_pixmap_qt_object(self) -> QGraphicsPixmapItem:
        pixmap = QPixmap()
        load_success = pixmap.load(self._resolved_path)
        if not load_success:
            raise ImageLoadingError(f"Failed to load image at {self.file_path}")
        qt_object = QGraphicsPixmapItem(pixmap)
        qt_object.setTransformationMode(_QT_SMOOTH_TRANSFORMATION)
        self._apply_common_properties(qt_object)
        return qt_object

    def _apply_common_properties(self, qt_object: QGraphicsItem):
        qt_object.setPos(point_to_qt_point_f(self.pos))
        if self.transform_origin != ORIGIN:
            qt_object.setTransformOriginPoint(
                point_to_qt_point_f(self.transform_origin)
            )
        if self.scale != 1:
            qt_object.setScale(self.scale)
        if self.rotation != 0:
            qt_object.setRotation(self.rotation)
        if self.transform_origin != ORIGIN:
            qt_object.setTransformOriginPoint(
                point_to_qt_point_f(self.transform_origin)
            )
        if self.opacity != 1:
            qt_object.setOpacity(self.opacity)

    def render(self):
        if self.file_path.suffix == ".svg":
            qt_object = self._create_svg_qt_object()
        else:
            qt_object = self._create_pixmap_qt_object()
        self._register_qt_object(qt_object)
