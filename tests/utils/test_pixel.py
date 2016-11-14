import unittest

from brown.utils.base_unit import BaseUnit
from brown.utils.pixel import Pixel


class TestPixel(unittest.TestCase):

    def test_pixel_base_unit_conversion(self):
        self.assertAlmostEqual(BaseUnit(Pixel(1)), BaseUnit(1))
        self.assertAlmostEqual(BaseUnit(Pixel(2)), BaseUnit(2))

    def test__str__(self):
        assert(str(Pixel(1)) == '1 pixels')
