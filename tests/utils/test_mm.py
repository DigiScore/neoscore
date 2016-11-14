import unittest

from brown.utils.base_unit import BaseUnit
from brown.utils.mm import Mm


class TestMm(unittest.TestCase):

    def test_mm_base_unit_conversion(self):
        self.assertAlmostEqual(BaseUnit(Mm(1)), BaseUnit(11.8110236))
        self.assertAlmostEqual(BaseUnit(Mm(2)), BaseUnit(23.6220472))

    def test__str__(self):
        assert(str(Mm(1)) == '1 millimeters')
