import unittest

from brown.utils.unit import Unit
from brown.utils.mm import Mm


class TestMm(unittest.TestCase):

    def test_mm_unit_conversion(self):
        self.assertAlmostEqual(Unit(Mm(1)), Unit(11.8110236))
        self.assertAlmostEqual(Unit(Mm(2)), Unit(23.6220472))

    def test__str__(self):
        assert(str(Mm(1)) == '1 millimeters')
