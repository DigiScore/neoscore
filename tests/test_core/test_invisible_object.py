import unittest

from neoscore.core import neoscore
from neoscore.core.invisible_object import InvisibleObject
from neoscore.utils.units import GraphicUnit, Unit


class TestInvisibleObject(unittest.TestCase):
    def setUp(self):
        neoscore.setup()

    def test_init(self):
        mock_parent = InvisibleObject((Unit(10), Unit(11)), parent=None)
        test_object = InvisibleObject((Unit(5), Unit(6)), parent=mock_parent)
        assert test_object.x == GraphicUnit(5)
        assert test_object.y == GraphicUnit(6)
        assert test_object.parent == mock_parent
