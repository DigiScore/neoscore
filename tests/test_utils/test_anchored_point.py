import os
import unittest
from nose.tools import assert_raises

from brown.core import brown
from brown.config import config
from brown.core.font import Font
from brown.core.text_object import TextObject
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
        self.test_parent = TextObject((5, 6), 'a', self.font)

    def test_init(self):
        test_point = AnchoredPoint(5, 6, self.test_parent)
        assert(test_point.x == 5)
        assert(test_point.y == 6)
        assert(test_point.parent == self.test_parent)

    def test_from_existing(self):
        original = AnchoredPoint(5, 6, 'mock parent')
        clone = AnchoredPoint.from_existing(original)
        # id() check may fail on non-CPython interpreters
        assert(id(original) != id(clone))
        assert(original.x == clone.x)
        assert(original.y == clone.y)
        assert(original.parent == clone.parent)

    def test_to_unit(self):
        test_point = AnchoredPoint(5, 6, self.test_parent).to_unit(Unit)
        assert(isinstance(test_point.x, Unit))
        assert(isinstance(test_point.y, Unit))
        assert(test_point.x == Unit(5))
        assert(test_point.y == Unit(6))
        assert(test_point.parent == self.test_parent)

    def test_indexing_with_invalid_raises_IndexError(self):
        test_point = AnchoredPoint(5, 6, self.test_parent)
        with assert_raises(IndexError):
            test_point[3]
        with assert_raises(IndexError):
            test_point[-1]
        with assert_raises(TypeError):
            test_point['nonsense index']

    def test_setters_hook_parent_setter_hook(self):

        class AnchoredPointHolder:
            def __init__(self, parent):
                self.point_setter_hook_called = False
                self.point = AnchoredPoint(0, 0, parent)
                self.point.setters_hook = self.handle_hook

            def handle_hook(self):
                self.point_setter_hook_called = True

        test_instance = AnchoredPointHolder(self.test_parent)
        assert(test_instance.point.parent == self.test_parent)
        test_instance.point.parent = TextObject((5, 6), 'a', self.font)
        assert(test_instance.point_setter_hook_called is True)

    def test_setters_hook_parent_setter_hook_with_same_value_set(self):

        class AnchoredPointHolder:
            def __init__(self, parent):
                self.point_setter_hook_called = False
                self.point = AnchoredPoint(0, 0, parent)
                self.point.setters_hook = self.handle_hook

            def handle_hook(self):
                self.point_setter_hook_called = True

        test_instance = AnchoredPointHolder(self.test_parent)
        assert(test_instance.point.parent == self.test_parent)
        test_instance.point.parent = self.test_parent
        assert(test_instance.point_setter_hook_called is True)

    def test__eq__(self):
        test_point = AnchoredPoint(5, 6, self.test_parent)
        test_point_eq = AnchoredPoint(5, 6, self.test_parent)
        test_point_ne_1 = AnchoredPoint(1, 6, self.test_parent)
        test_point_ne_2 = AnchoredPoint(5, 7, self.test_parent)
        test_point_ne_3 = AnchoredPoint(5, 7, None)
        assert(test_point == test_point_eq)
        assert(test_point != test_point_ne_1)
        assert(test_point != test_point_ne_2)
        assert(test_point != test_point_ne_3)

    def test__add__(self):
        p1 = AnchoredPoint(1, 2, None)
        p2 = AnchoredPoint(3, 4, None)
        p3 = AnchoredPoint(5, 6, self.test_parent)
        p4 = AnchoredPoint(7, 8, self.test_parent)
        assert(p1 + p2 == AnchoredPoint(4, 6, None))
        assert(p3 + p4 == AnchoredPoint(12, 14, self.test_parent))
        with assert_raises(TypeError):
            p2 + p3
        with assert_raises(TypeError):
            p2 + 5

    def test__sub__(self):
        p1 = AnchoredPoint(1, 2, None)
        p2 = AnchoredPoint(3, 4, None)
        p3 = AnchoredPoint(5, 6, self.test_parent)
        p4 = AnchoredPoint(7, 8, self.test_parent)
        assert(p1 - p2 == AnchoredPoint(-2, -2, None))
        assert(p3 - p4 == AnchoredPoint(-2, -2, self.test_parent))
        with assert_raises(TypeError):
            p2 - p3
        with assert_raises(TypeError):
            p2 - 5

    def test__mult__(self):
        p1 = AnchoredPoint(1, 2, None)
        assert(p1 * -1) == AnchoredPoint(-1, -2, None)
        p2 = AnchoredPoint(Unit(2), Unit(3), None)
        assert(p2 * Unit(-1) == AnchoredPoint(Unit(-2), Unit(-3), None))
