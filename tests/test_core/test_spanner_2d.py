import unittest

from brown.core import brown
from brown.core.graphic_object import GraphicObject
from brown.core.invisible_object import InvisibleObject
from brown.core.spanner_2d import Spanner2D
from brown.utils.point import Point
from brown.utils.units import Unit

from ..helpers import assert_almost_equal


class MockSpanner2D(GraphicObject, Spanner2D):

    """A mock spanner for testing."""

    def __init__(self, pos, parent, end_pos, end_parent):
        GraphicObject.__init__(self, pos, parent=parent)
        Spanner2D.__init__(self, end_pos, end_parent or self)


class TestSpanner2D(unittest.TestCase):
    def setUp(self):
        brown.setup()

    def end_y_settable(self):
        spanner = MockSpanner2D(
            Point(Unit(0), Unit(1)), None, Point(Unit(2), Unit(3)), None
        )
        assert spanner.end_pos == Point(Unit(2), Unit(3))
        spanner.end_y = Unit(10)
        assert spanner.end_pos == Point(Unit(2), Unit(10))

    def end_pos_settable(self):
        spanner = MockSpanner2D(
            Point(Unit(0), Unit(1)), None, Point(Unit(2), Unit(3)), None
        )
        spanner.end_pos = Point(Unit(12), Unit(34))
        assert spanner.end_pos == Point(Unit(12), Unit(34))

    def test_length_no_parents(self):
        spanner = MockSpanner2D(
            Point(Unit(1), Unit(2)),
            brown.document.pages[0],
            Point(Unit(5), Unit(7)),
            brown.document.pages[0],
        )
        # math.sqrt(((5-1)**2) + ((7-2)**2))
        assert_almost_equal(spanner.spanner_2d_length, Unit(6.4031242374328485))

    def test_length_with_self_parent(self):
        parent = MockSpanner2D(
            Point(Unit(1), Unit(2)), None, Point(Unit(0), Unit(0)), None
        )
        spanner = MockSpanner2D(
            Point(Unit(3), Unit(7)), parent, Point(Unit(4), Unit(5)), None
        )
        # math.sqrt((4**2) + (5**2))
        assert_almost_equal(spanner.spanner_2d_length, Unit(6.4031242374328485))

    def test_length_with_parents(self):
        parent_1 = InvisibleObject((Unit(1), Unit(2)), None)
        parent_2 = InvisibleObject((Unit(11), Unit(12)), None)
        spanner = MockSpanner2D(
            Point(Unit(1), Unit(2)), parent_1, Point(Unit(4), Unit(5)), parent_2
        )
        # math.sqrt(((15-2)**2) + ((17-4)**2))
        assert_almost_equal(spanner.spanner_2d_length, Unit(18.384776310850235))
