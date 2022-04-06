import pytest

from neoscore.core.painted_object import PaintedObject
from neoscore.core.point import Point
from neoscore.core.spanner import Spanner
from neoscore.core.units import ZERO, Unit

from ..helpers import AppTest


class MockSpanner(PaintedObject, Spanner):

    """A mock spanner for testing."""

    def __init__(self, pos, parent, end_x, end_parent):
        PaintedObject.__init__(self, pos, parent=parent)
        Spanner.__init__(self, end_x, end_parent or self)


class TestSpanner(AppTest):
    def test_end_y_with_end_parent_self(self):
        spanner = MockSpanner(Point(Unit(20), Unit(5)), None, Unit(30), None)
        assert spanner.end_y == ZERO
        assert spanner.end_pos == Point(Unit(30), ZERO)
        assert spanner.end_parent == spanner

    def test_end_y_with_other_end_parent(self):
        end_parent = PaintedObject(Point(Unit(10), Unit(10)))
        spanner = MockSpanner(Point(Unit(20), Unit(5)), None, Unit(30), end_parent)
        assert spanner.end_y == Unit(-5)
        assert spanner.end_pos == Point(Unit(30), Unit(-5))

    def test_end_y_not_settable(self):
        with pytest.raises(AttributeError):
            spanner = MockSpanner(Point(Unit(20), Unit(5)), None, Unit(30), None)
            spanner.end_y = ZERO

    def test_end_pos_not_settable(self):
        with pytest.raises(AttributeError):
            spanner = MockSpanner(Point(Unit(20), Unit(5)), None, Unit(30), None)
            spanner.end_pos = ZERO
