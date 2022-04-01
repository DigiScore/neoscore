from neoscore.core import neoscore
from neoscore.core.path import Path
from neoscore.core.text import Text
from neoscore.utils.color import Color
from neoscore.utils.point import ORIGIN

from ..helpers import AppTest


class TestNeoscore(AppTest):
    def test_setting_global_color(self):
        text_created_before_set = Text(ORIGIN, None, "Test")
        path_created_before_set = Path(ORIGIN, None)

        neoscore.set_default_color(Color(255, 0, 0))

        text_created_after_set = Text(ORIGIN, None, "Test")
        path_created_after_set = Path(ORIGIN, None)

        assert text_created_before_set.brush.color == Color(0, 0, 0)
        assert path_created_before_set.brush.color == Color(0, 0, 0)
        assert path_created_before_set.pen.color == Color(0, 0, 0)

        assert text_created_after_set.brush.color == Color(255, 0, 0)
        assert path_created_after_set.brush.color == Color(255, 0, 0)
        assert path_created_after_set.pen.color == Color(255, 0, 0)
