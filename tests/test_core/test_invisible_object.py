import unittest

from brown.core import brown
from brown.core.invisible_object import InvisibleObject
from brown.utils.units import GraphicUnit


class TestInvisibleObject(unittest.TestCase):
    def setUp(self):
        brown.setup()

    def test_init(self):
        mock_parent = InvisibleObject((10, 11), parent=None)
        test_object = InvisibleObject((5, 6), parent=mock_parent)
        assert test_object.x == GraphicUnit(5)
        assert test_object.y == GraphicUnit(6)
        assert test_object.parent == mock_parent
