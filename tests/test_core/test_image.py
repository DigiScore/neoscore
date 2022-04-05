import pathlib

from neoscore.core.image import Image
from neoscore.core.point import ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Unit

from ..helpers import AppTest, render_scene

# Fake path for unit tests
fake_path = pathlib.Path("/some/file/path.png")

# Real paths for integration tests
img_dir = (pathlib.Path(__file__).parent / ".." / "resources").resolve()
pixmap_image_path = img_dir / "pixmap_image.png"
svg_image_path = img_dir / "svg_image.svg"


class TestImage(AppTest):
    def test_init(self):
        parent = PositionedObject(ORIGIN)
        image = Image((Unit(5), Unit(6)), parent, fake_path, 2)
        assert image.pos == Point(Unit(5), Unit(6))
        assert image.parent == parent
        assert image.file_path == fake_path
        assert image.scale == 2

    def test_init_with_str_file_path(self):
        image = Image((Unit(5), Unit(6)), None, str(fake_path), 2)
        assert image.file_path == fake_path

    def test_scale_setter(self):
        image = Image(ORIGIN, None, fake_path)
        image.scale = 3
        assert image.scale == 3

    def test_file_path_setter_with_pathlib_path(self):
        image = Image(ORIGIN, None, "/test/path")
        image.file_path = fake_path
        assert image.file_path == fake_path

    def test_file_path_setter_with_str_path(self):
        image = Image(ORIGIN, None, "/test/path")
        image.file_path = "another/test/path"
        assert image.file_path == pathlib.Path("another/test/path")

    def test_length_is_zero(self):
        image = Image(ORIGIN, None, "/test/path")
        assert image.breakable_length == ZERO

    def test_pixmap_image_end_to_end(self):
        Image(ORIGIN, None, pixmap_image_path, 2)
        render_scene()

    def test_svg_image_end_to_end(self):
        Image(ORIGIN, None, svg_image_path, 2)
        render_scene()
