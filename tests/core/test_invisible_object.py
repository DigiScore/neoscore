import unittest

from brown.core import brown
from brown.core.invisible_object import InvisibleObject

from mock_graphic_object import MockGraphicObject


class TestInvisibleObject(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_init(self):
        mock_parent = MockGraphicObject(10, 11, parent=None)
        test_object = InvisibleObject(5, 6, parent=mock_parent)
        assert(test_object.x == 5)
        assert(test_object.y == 6)
        assert(test_object.parent == mock_parent)

    def test_default_init_values(self):
        # API default values canary
        test_object = InvisibleObject(5, 6)
        assert(test_object.parent is None)
