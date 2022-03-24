import pathlib
from dataclasses import dataclass
from typing import Any

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

from neoscore.core import neoscore
from neoscore.interface.positioned_object_interface import PositionedObjectInterface
from neoscore.interface.qt.converters import point_to_qt_point_f
from neoscore.utils.exceptions import ImageLoadingError

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

    scale: float = 1

    def _create_svg_qt_object(self) -> Any:  # todo
        raise NotImplemented

    def _create_pixmap_qt_object(self) -> QGraphicsPixmapItem:
        pixmap = QPixmap()
        load_success = pixmap.load(str(self.file_path.expanduser()))
        if not load_success:
            raise ImageLoadingError(f"Failed to load image at {self.file_path}")
        qt_object = QGraphicsPixmapItem(pixmap)
        qt_object.setTransformationMode(_QT_SMOOTH_TRANSFORMATION)
        qt_object.setPos(point_to_qt_point_f(self.pos))
        if self.scale != 1:
            qt_object.setScale(self.scale)
        return qt_object

    def render(self):
        if self.file_path.suffix == ".svg":
            qt_object = self._create_svg_qt_object()
        else:
            qt_object = self._create_pixmap_qt_object()
        neoscore._app_interface.scene.addItem(qt_object)
