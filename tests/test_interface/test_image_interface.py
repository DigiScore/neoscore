import pathlib

from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import Unit
from neoscore.interface.image_interface import ImageInterface
from neoscore.interface.qt.converters import point_to_qt_point_f

from ..helpers import AppTest

img_dir = (pathlib.Path(__file__).parent / ".." / "resources").resolve()
pixmap_image_path = img_dir / "pixmap_image.png"
svg_image_path = img_dir / "svg_image.svg"


class TestImageInterface(AppTest):
    def test_pixmap_image_loading(self):
        interface = ImageInterface(
            Point(Unit(5), Unit(6)), None, 1, 0, ORIGIN, pixmap_image_path
        )
        interface.render()

    def test_pixmap_qt_item_properties(self):
        transform_origin = Point(Unit(12), Unit(12))
        interface = ImageInterface(
            Point(Unit(5), Unit(6)),
            None,
            2,
            3,
            transform_origin,
            pixmap_image_path,
            0.6,
        )
        qt_object = interface._create_pixmap_qt_object()
        assert qt_object.x() == 5
        assert qt_object.y() == 6
        assert qt_object.scale() == 2
        assert qt_object.rotation() == 3
        assert qt_object.transformOriginPoint() == point_to_qt_point_f(transform_origin)
        assert qt_object.opacity() == 0.6

    def test_pixmap_qt_object_transformation_mode(self):
        interface = ImageInterface(
            Point(Unit(5), Unit(6)), None, 1, 0, ORIGIN, pixmap_image_path
        )
        qt_object = interface._create_pixmap_qt_object()
        assert qt_object.transformationMode() == 1  # Qt::SmoothTransformation

    def test_svg_image_loading(self):
        interface = ImageInterface(
            Point(Unit(5), Unit(6)), None, 1, 1, ORIGIN, svg_image_path
        )
        interface.render()

    def test_svg_qt_item_properties(self):
        transform_origin = Point(Unit(12), Unit(12))
        interface = ImageInterface(
            Point(Unit(5), Unit(6)), None, 2, 3, transform_origin, svg_image_path, 0.6
        )
        qt_object = interface._create_svg_qt_object()
        assert qt_object.x() == 5
        assert qt_object.y() == 6
        assert qt_object.scale() == 2
        assert qt_object.rotation() == 3
        assert qt_object.transformOriginPoint() == point_to_qt_point_f(transform_origin)
        assert qt_object.opacity() == 0.6
