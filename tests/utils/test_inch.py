import unittest

from brown.utils.unit import Unit
from brown.utils.inch import Inch


class TestInch(unittest.TestCase):

    def test_inch_unit_conversion(self):
        self.assertAlmostEqual(Unit(Inch(1)), Unit(300))
        self.assertAlmostEqual(Unit(Inch(2)), Unit(600))

    def test__str__(self):
        assert(str(Inch(1)) == '1 inches')
