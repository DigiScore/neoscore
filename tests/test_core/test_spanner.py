import unittest

from brown.core import brown
from brown.core.graphic_object import GraphicObject
from brown.core.invisible_object import InvisibleObject
from brown.core.spanner import Spanner
from brown.utils.point import Point
from brown.utils.units import Unit

from ..helpers import assert_almost_equal


class MockSpanner(GraphicObject, Spanner):

    """A mock spanner for testing."""

    def __init__(self, pos, parent, end_pos, end_parent):
        GraphicObject.__init__(self, pos, parent=parent)
        Spanner.__init__(self, end_pos, end_parent)


class TestSpanner(unittest.TestCase):
    def setUp(self):
        brown.setup()

    def test_inputs_converted_to_parent_points(self):
        spanner = MockSpanner(
            Point(Unit(0), Unit(1)), None, Point(Unit(2), Unit(3)), None
        )
        assert spanner.end_pos == Point(Unit(2), Unit(3))
        assert spanner.end_parent == spanner

    def test_length_no_parents(self):
        spanner = MockSpanner(
            Point(Unit(1), Unit(2)),
            brown.document.pages[0],
            Point(Unit(5), Unit(7)),
            brown.document.pages[0],
        )
        # math.sqrt(((5-1)**2) + ((7-2)**2))
        assert_almost_equal(spanner.spanner_length, Unit(6.4031242374328485))

    def test_length_with_self_parent(self):
        parent = MockSpanner(
            Point(Unit(1), Unit(2)), None, Point(Unit(0), Unit(0)), None
        )
        spanner = MockSpanner(
            Point(Unit(3), Unit(7)), parent, Point(Unit(4), Unit(5)), None
        )
        # math.sqrt((4**2) + (5**2))
        assert_almost_equal(spanner.spanner_length, Unit(6.4031242374328485))

    def test_length_with_parents(self):
        parent_1 = InvisibleObject((Unit(1), Unit(2)), None)
        parent_2 = InvisibleObject((Unit(11), Unit(12)), None)
        spanner = MockSpanner(
            Point(Unit(1), Unit(2)), parent_1, Point(Unit(4), Unit(5)), parent_2
        )
        # math.sqrt(((15-2)**2) + ((17-4)**2))
        assert_almost_equal(spanner.spanner_length, Unit(18.384776310850235))

    def test_set_end_pos(self):
        spanner = MockSpanner(
            Point(Unit(1), Unit(2)), None, Point(Unit(4), Unit(5)), None
        )
        spanner.end_pos = Point(Unit(0), Unit(1))
        assert spanner.end_pos == Point(Unit(0), Unit(1))

    def test_set_end_x(self):
        spanner = MockSpanner(
            Point(Unit(1), Unit(2)), None, Point(Unit(4), Unit(5)), None
        )
        spanner.end_x = Unit(999)
        assert spanner.end_x == Unit(999)
        assert spanner.end_pos == Point(Unit(999), Unit(5))

    def test_set_end_y(self):
        spanner = MockSpanner(
            Point(Unit(1), Unit(2)), None, Point(Unit(4), Unit(5)), None
        )
        spanner.end_y = Unit(999)
        assert spanner.end_y == Unit(999)
        assert spanner.end_pos == Point(Unit(4), Unit(999))
