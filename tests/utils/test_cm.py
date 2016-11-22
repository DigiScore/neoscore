import unittest

from brown.utils.units import Unit, Cm


class TestCm(unittest.TestCase):

    def test_cm_unit_conversion(self):
        self.assertAlmostEqual(Unit(Cm(1)), Unit(1.18110236220472))
        self.assertAlmostEqual(Unit(Cm(2)), Unit(2.36220472440944))

    def test__str__(self):
        assert(str(Cm(1)) == '1 centimeters')
