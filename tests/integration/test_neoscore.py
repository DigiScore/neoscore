from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.color import Color
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN
from neoscore.core.text import Text

from ..helpers import AppTest


class TestNeoscore(AppTest):
    def test_setting_global_color(self):
        initial_color = Pen._default_color
        try:
            text_created_before_set = Text(ORIGIN, None, "Test")
            path_created_before_set = Path(ORIGIN, None)

            neoscore.set_default_color(Color(1, 2, 3))

            text_created_after_set = Text(ORIGIN, None, "Test")
            path_created_after_set = Path(ORIGIN, None)

            assert text_created_before_set.brush.color == Color(0, 0, 0)
            assert path_created_before_set.brush.color == Color(0, 0, 0)
            assert path_created_before_set.pen.color == Color(0, 0, 0)

            assert text_created_after_set.brush.color == Color(1, 2, 3)
            assert path_created_after_set.brush.color == Color(1, 2, 3)
            assert path_created_after_set.pen.color == Color(1, 2, 3)
        finally:
            neoscore.set_default_color(initial_color)

    def test_set_background_brush(self):
        assert neoscore.background_brush == Brush("#ffffff")
        new_brush = Brush("#ffff00")
        neoscore.set_background_brush(new_brush)
        assert neoscore.background_brush == new_brush
        assert neoscore.app_interface.background_brush == new_brush.interface
