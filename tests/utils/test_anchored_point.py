import os
import unittest
import pytest

from brown.core import brown
from brown.config import config
from brown.core.font import Font
from brown.core.glyph import Glyph
from brown.utils.anchored_point import AnchoredPoint
from brown.utils.units import Unit, Mm


class TestAnchoredPoint(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.test_font_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        self.font_id = brown._app_interface.register_font(
            self.test_font_file_path)
        self.font = Font('Bravura', 12, 1, False)
        self.test_parent = Glyph((5, 6), 'a', self.font)

    def test_init_with_triple(self):
        test_point = AnchoredPoint(5, 6, self.test_parent)
        assert(test_point.x == 5)
        assert(test_point.y == 6)
        assert(test_point.parent == self.test_parent)

    def test_init_with_3_tuple(self):
        test_point = AnchoredPoint((5, 6, self.test_parent))
        assert(test_point.x == 5)
        assert(test_point.y == 6)
        assert(test_point.parent == self.test_parent)

    def test_init_with_existing_AnchoredPoint(self):
        existing_point = AnchoredPoint(5, 6, self.test_parent)
        test_point = AnchoredPoint(existing_point)
        assert(test_point.x == 5)
        assert(test_point.y == 6)
        assert(test_point.parent == self.test_parent)

    def test_init_with_unit(self):
        test_point = AnchoredPoint.with_unit(5, 6, self.test_parent, unit=Unit)
        assert(isinstance(test_point.x, Unit))
        assert(isinstance(test_point.y, Unit))
        assert(test_point.x == Unit(5))
        assert(test_point.y == Unit(6))
        assert(test_point.parent == self.test_parent)

    def test_with_unit_fails_if_unit_not_set(self):
        with pytest.raises(TypeError):
            AnchoredPoint.with_unit(5, 6, self.test_parent)

    def test_indexing_with_invalid_raises_IndexError(self):
        test_point = AnchoredPoint(5, 6, self.test_parent)
        with pytest.raises(IndexError):
            test_point[3]
        with pytest.raises(IndexError):
            test_point[-1]
        with pytest.raises(TypeError):
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
        test_instance.point.parent = Glyph((5, 6), 'a', self.font)
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
