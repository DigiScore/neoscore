import pathlib
import unittest

from neoscore.core import neoscore
from neoscore.core.image import Image
from neoscore.core.positioned_object import PositionedObject
from neoscore.utils.point import ORIGIN, Point
from neoscore.utils.units import ZERO, Unit

# Since this suite doesn't actually render, the path doesn't need to be valid
pixmap_image_path = pathlib.Path("/some/file/path.png")


class TestImage(unittest.TestCase):
    def setUp(self):
        neoscore.setup()

    def test_init(self):
        parent = PositionedObject(ORIGIN)
        image = Image((Unit(5), Unit(6)), parent, pixmap_image_path, 2)
        assert image.pos == Point(Unit(5), Unit(6))
        assert image.parent == parent
        assert image.file_path == pixmap_image_path
        assert image.scale == 2

    def test_init_with_str_file_path(self):
        image = Image((Unit(5), Unit(6)), None, str(pixmap_image_path), 2)
        assert image.file_path == pixmap_image_path

    def test_scale_setter(self):
        image = Image(ORIGIN, None, pixmap_image_path)
        image.scale = 3
        assert image.scale == 3

    def test_file_path_setter_with_pathlib_path(self):
        image = Image(ORIGIN, None, "/test/path")
        image.file_path = pixmap_image_path
        assert image.file_path == pixmap_image_path

    def test_file_path_setter_with_str_path(self):
        image = Image(ORIGIN, None, "/test/path")
        image.file_path = "another/test/path"
        assert image.file_path == pathlib.Path("another/test/path")

    def test_length_is_zero(self):
        image = Image(ORIGIN, None, "/test/path")
        assert image.length == ZERO
