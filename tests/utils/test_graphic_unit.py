import unittest

from brown.utils.unit import Unit
from brown.utils.graphic_unit import GraphicUnit


class TestGraphicUnit(unittest.TestCase):

    def test_graphic_unit_unit_conversion(self):
        self.assertAlmostEqual(Unit(GraphicUnit(1)), Unit(1))
        self.assertAlmostEqual(Unit(GraphicUnit(2)), Unit(2))

    def test__str__(self):
        assert(str(GraphicUnit(1)) == '1 pixels')
