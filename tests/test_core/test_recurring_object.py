import unittest

from brown.core import brown
from brown.core.recurring_object import RecurringObject
from brown.utils.units import Unit


class TestRecurringObject(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_find_x_in_line(self):
        assert(RecurringObject(0)._find_x_in_line(Unit(100)) == Unit(0))
        assert(RecurringObject(-1)._find_x_in_line(Unit(100)) == Unit(-1))
        assert(RecurringObject(1)._find_x_in_line(Unit(100)) == Unit(1))
