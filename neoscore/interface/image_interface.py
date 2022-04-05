import pathlib
from dataclasses import dataclass
from typing import Any

from PyQt5.QtGui import QPixmap
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import QGraphicsPixmapItem

from neoscore.core import neoscore
from neoscore.core.exceptions import ImageLoadingError
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

    scale: float = 1

    @property
    def _resolved_path(self) -> str:
        return str(self.file_path.expanduser())

    def _create_svg_qt_object(self) -> Any:  # todo
        qt_object = QGraphicsSvgItem(self._resolved_path)
        qt_object.setPos(point_to_qt_point_f(self.pos))
        if self.scale != 1:
            qt_object.setScale(self.scale)
        return qt_object

    def _create_pixmap_qt_object(self) -> QGraphicsPixmapItem:
        pixmap = QPixmap()
        load_success = pixmap.load(self._resolved_path)
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
