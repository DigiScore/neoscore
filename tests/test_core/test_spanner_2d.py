from neoscore.core.painted_object import PaintedObject
from neoscore.core.point import ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner_2d import Spanner2D
from neoscore.core.units import Unit

from ..helpers import AppTest, assert_almost_equal


class MockSpanner2D(PaintedObject, Spanner2D):

    """A mock spanner for testing."""

    def __init__(self, pos, parent, end_pos, end_parent):
        PaintedObject.__init__(self, pos, parent=parent)
        Spanner2D.__init__(self, end_pos, end_parent or self)


class TestSpanner2D(AppTest):
    def test_end_pos_point_def_supported(self):
        spanner = MockSpanner2D((Unit(0), Unit(1)), None, Point(Unit(2), Unit(3)), None)
        assert spanner.end_pos == Point(Unit(2), Unit(3))

    def test_end_y_settable(self):
        spanner = MockSpanner2D(
            Point(Unit(0), Unit(1)), None, Point(Unit(2), Unit(3)), None
        )
        assert spanner.end_pos == Point(Unit(2), Unit(3))
        spanner.end_y = Unit(10)
        assert spanner.end_pos == Point(Unit(2), Unit(10))

    def test_end_pos_settable(self):
        spanner = MockSpanner2D(
            Point(Unit(0), Unit(1)), None, Point(Unit(2), Unit(3)), None
        )
        spanner.end_pos = Point(Unit(12), Unit(34))
        assert spanner.end_pos == Point(Unit(12), Unit(34))
        spanner.end_pos = (Unit(123), Unit(456))
        assert spanner.end_pos == Point(Unit(123), Unit(456))

    def test_length_with_no_end_parent(self):
        spanner = MockSpanner2D(
            Point(Unit(3), Unit(7)), None, Point(Unit(4), Unit(5)), None
        )
        # math.sqrt((4**2) + (5**2))
        assert_almost_equal(spanner.spanner_2d_length, Unit(6.4031242374328485))

    def test_length_with_end_parent(self):
        parent_1 = PositionedObject((Unit(1), Unit(2)), None)
        parent_2 = PositionedObject((Unit(11), Unit(12)), None)
        spanner = MockSpanner2D(
            Point(Unit(1), Unit(2)), parent_1, Point(Unit(4), Unit(5)), parent_2
        )
        # math.sqrt(((15-2)**2) + ((17-4)**2))
        assert_almost_equal(spanner.spanner_2d_length, Unit(18.384776310850235))

    def test_angle_with_no_end_parent(self):
        spanner = MockSpanner2D(
            Point(Unit(3), Unit(7)), None, Point(Unit(4), Unit(5)), None
        )
        self.assertAlmostEqual(spanner.angle, 51.34019174590991)

    def test_angle_with_end_parent(self):
        parent_1 = PositionedObject((Unit(1), Unit(2)), None)
        parent_2 = PositionedObject((Unit(11), Unit(12)), None)
        spanner = MockSpanner2D(
            Point(Unit(1), Unit(2)), parent_1, Point(Unit(4), Unit(5)), parent_2
        )
        self.assertAlmostEqual(spanner.angle, 45.0)

    def test_point_along_spanner(self):
        parent_1 = PositionedObject((Unit(1), Unit(2)), None)
        parent_2 = PositionedObject((Unit(11), Unit(12)), None)
        spanner = MockSpanner2D(
            Point(Unit(1), Unit(2)), parent_1, Point(Unit(4), Unit(5)), parent_2
        )

        assert_almost_equal(spanner.point_along_spanner(0), ORIGIN)
        base_delta = Point(Unit(10 - 1 + 4), Unit(10 - 2 + 5))
        assert_almost_equal(spanner.point_along_spanner(1), base_delta)
        assert_almost_equal(spanner.point_along_spanner(0.5), base_delta * 0.5)
        # Values outside the spanner should give points as if
        # the spanner extends to infinity
        assert_almost_equal(spanner.point_along_spanner(2), base_delta * 2)
        assert_almost_equal(spanner.point_along_spanner(-1), base_delta * -1)
