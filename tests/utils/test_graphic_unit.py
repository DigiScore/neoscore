import unittest

from brown.utils.base_unit import BaseUnit
from brown.utils.graphic_unit import GraphicUnit


class TestGraphicUnit(unittest.TestCase):

    def test_graphic_unit_base_unit_conversion(self):
        self.assertAlmostEqual(BaseUnit(GraphicUnit(1)), BaseUnit(1))
        self.assertAlmostEqual(BaseUnit(GraphicUnit(2)), BaseUnit(2))

    def test__str__(self):
        assert(str(GraphicUnit(1)) == '1 pixels')
