import pytest

from neoscore.core.point import ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner import Spanner
from neoscore.core.units import ZERO, Unit

from ..helpers import AppTest, assert_almost_equal


class MockSpanner(Spanner, PositionedObject):

    """A mock spanner for testing."""

    def __init__(self, pos, parent, end_x, end_parent):
        PositionedObject.__init__(self, pos, parent=parent)
        Spanner.__init__(self, end_x, end_parent or self)


class TestSpanner(AppTest):
    def test_end_y_with_end_parent_self(self):
        spanner = MockSpanner((Unit(20), Unit(5)), None, Unit(30), None)
        assert spanner.end_y == ZERO
        assert spanner.end_pos == Point(Unit(30), ZERO)
        assert spanner.end_parent == spanner

    def test_end_y_with_other_end_parent(self):
        end_parent = PositionedObject(Point(Unit(10), Unit(10)), None)
        spanner = MockSpanner((Unit(20), Unit(5)), None, Unit(30), end_parent)
        assert spanner.end_y == Unit(-5)
        assert spanner.end_pos == Point(Unit(30), Unit(-5))

    def test_end_y_not_settable(self):
        with pytest.raises(AttributeError):
            spanner = MockSpanner((Unit(20), Unit(5)), None, Unit(30), None)
            spanner.end_y = ZERO  # noqa

    def test_end_pos_not_settable(self):
        with pytest.raises(AttributeError):
            spanner = MockSpanner((Unit(20), Unit(5)), None, Unit(30), None)
            spanner.end_pos = ZERO  # noqa

    def test_point_along_spanner(self):
        end_parent = PositionedObject((Unit(10), Unit(10)), None)
        spanner = MockSpanner((Unit(20), Unit(5)), None, Unit(30), end_parent)
        assert_almost_equal(spanner.point_along_spanner(0), ORIGIN)
        assert_almost_equal(spanner.point_along_spanner(1), Point(Unit(30 - 10), ZERO))
        assert_almost_equal(
            spanner.point_along_spanner(0.5), Point(Unit(30 - 10) / 2, ZERO)
        )
        # Values outside the spanner should give points as if
        # the spanner extends to infinity
        assert_almost_equal(
            spanner.point_along_spanner(2), Point(Unit(30 - 10) * 2, ZERO)
        )
        assert_almost_equal(
            spanner.point_along_spanner(-1), Point(-Unit(30 - 10), ZERO)
        )

    def test_breakable_length_method_resolution_order(self):
        class WrongMROSpanner(PositionedObject, Spanner):
            def __init__(self, pos, parent, end_x, end_parent):
                PositionedObject.__init__(self, pos, parent=parent)
                Spanner.__init__(self, end_x, end_parent or self)

        class RightMROSpanner(Spanner, PositionedObject):
            def __init__(self, pos, parent, end_x, end_parent):
                PositionedObject.__init__(self, pos, parent=parent)
                Spanner.__init__(self, end_x, end_parent or self)

        wrong_mro_spanner = WrongMROSpanner((Unit(20), Unit(5)), None, Unit(30), None)
        right_mro_spanner = RightMROSpanner((Unit(20), Unit(5)), None, Unit(30), None)
        assert wrong_mro_spanner.breakable_length == ZERO
        assert right_mro_spanner.breakable_length == Unit(30)
