import unittest

from brown.utils.base_unit import BaseUnit
from brown.utils.inch import Inch


class TestInch(unittest.TestCase):

    def test_inch_base_unit_conversion(self):
        self.assertAlmostEqual(BaseUnit(Inch(1)), BaseUnit(300))
        self.assertAlmostEqual(BaseUnit(Inch(2)), BaseUnit(600))

    def test__str__(self):
        assert(str(Inch(1)) == '1 inches')
