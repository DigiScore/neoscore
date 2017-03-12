import os
import unittest

import pytest

from brown.core import brown
from brown import config
from brown.core.font import Font
from brown.core.text import Text
from brown.utils.anchored_point import AnchoredPoint
from brown.utils.units import Unit


class TestAnchoredPoint(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.test_font_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        self.font_id = brown._app_interface.register_font(
            self.test_font_file_path)
        self.font = Font('Bravura', 12, 1, False)
        self.test_parent = Text((5, 6), 'a', self.font)

    def test_init(self):
        test_point = AnchoredPoint(5, 6, 1, self.test_parent)
        assert(test_point.x == 5)
        assert(test_point.y == 6)
        assert(test_point.page == 1)
        assert(test_point.parent == self.test_parent)

    def test_page_defaults_to_0(self):
        assert(AnchoredPoint(1, 2).page == 0)

    def test_from_existing(self):
        original = AnchoredPoint(5, 6, 1, 'mock parent')
        clone = AnchoredPoint.from_existing(original)
        # id() check may fail on non-CPython interpreters
        assert(id(original) != id(clone))
        assert(original.x == clone.x)
        assert(original.y == clone.y)
        assert(original.page == clone.page)
        assert(original.parent == clone.parent)

    def test_to_unit(self):
        test_point = AnchoredPoint(5, 6, 1, self.test_parent).to_unit(Unit)
        assert(isinstance(test_point.x, Unit))
        assert(isinstance(test_point.y, Unit))
        assert(test_point.x == Unit(5))
        assert(test_point.y == Unit(6))
        assert(test_point.page == 1)
        assert(test_point.parent == self.test_parent)

    def test__eq__(self):
        test_point = AnchoredPoint(5, 6, 1, self.test_parent)
        test_point_eq = AnchoredPoint(5, 6, 1, self.test_parent)
        test_point_ne_1 = AnchoredPoint(1, 6, 1, self.test_parent)
        test_point_ne_2 = AnchoredPoint(5, 7, 1, self.test_parent)
        test_point_ne_3 = AnchoredPoint(5, 7, 1, None)
        test_point_ne_4 = AnchoredPoint(5, 6, 2, self.test_parent)
        assert(test_point == test_point_eq)
        assert(test_point != test_point_ne_1)
        assert(test_point != test_point_ne_2)
        assert(test_point != test_point_ne_3)
        assert(test_point != test_point_ne_3)
        assert(test_point != test_point_ne_4)

    def test__add__(self):
        p1 = AnchoredPoint(1, 2, 1, None)
        p2 = AnchoredPoint(3, 4, 2, None)
        p3 = AnchoredPoint(5, 6, 1, self.test_parent)
        p4 = AnchoredPoint(7, 8, 2, self.test_parent)
        assert(p1 + p2 == AnchoredPoint(4, 6, 3, None))
        assert(p3 + p4 == AnchoredPoint(12, 14, 3, self.test_parent))
        with pytest.raises(TypeError):
            p2 + p3
        with pytest.raises(TypeError):
            p2 + 5

    def test__sub__(self):
        p1 = AnchoredPoint(1, 2, 1, None)
        p2 = AnchoredPoint(3, 4, 2, None)
        p3 = AnchoredPoint(5, 6, 1, self.test_parent)
        p4 = AnchoredPoint(7, 8, 2, self.test_parent)
        assert(p1 - p2 == AnchoredPoint(-2, -2, -1, None))
        assert(p3 - p4 == AnchoredPoint(-2, -2, -1, self.test_parent))
        with pytest.raises(TypeError):
            p2 - p3
        with pytest.raises(TypeError):
            p2 - 5

    def test__mult__(self):
        p1 = AnchoredPoint(1, 2, 7, None)
        assert(p1 * -1) == AnchoredPoint(-1, -2, 7, None)
        p2 = AnchoredPoint(Unit(2), Unit(3), 7, None)
        assert(p2 * Unit(-1) == AnchoredPoint(Unit(-2), Unit(-3), 7, None))
