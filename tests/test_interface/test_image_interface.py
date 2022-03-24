import pathlib
import unittest

from neoscore.core import neoscore
from neoscore.interface.image_interface import ImageInterface
from neoscore.utils.point import Point
from neoscore.utils.units import Unit

img_dir = (pathlib.Path(__file__).parent / ".." / "resources").resolve()
pixmap_image_path = img_dir / "pixmap_image.png"


class TestImageInterface(unittest.TestCase):
    def setUp(self):
        neoscore.setup()

    def test_image_loading(self):
        interface = ImageInterface(Point(Unit(5), Unit(6)), pixmap_image_path, 1)
        interface.render()

    def test_qt_item_properties(self):
        interface = ImageInterface(Point(Unit(5), Unit(6)), pixmap_image_path, 2)
        qt_object = interface._create_pixmap_qt_object()
        assert qt_object.x() == 5
        assert qt_object.y() == 6
        assert qt_object.scale() == 2

    def test_qt_object_transformation_mode(self):
        interface = ImageInterface(Point(Unit(5), Unit(6)), pixmap_image_path, 2)
        qt_object = interface._create_pixmap_qt_object()
        assert qt_object.transformationMode() == 1  # Qt::SmoothTransformation
