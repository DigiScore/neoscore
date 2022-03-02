import unittest

from brown.core import brown
from brown.core.flowable import Flowable
from brown.core.graphic_object import GraphicObject
from brown.core.horizontal_spanner import HorizontalSpanner
from brown.utils.point import Point
from brown.utils.units import Unit


class MockHorizontalSpanner(GraphicObject, HorizontalSpanner):
    def __init__(self, pos, parent, end_x, end_parent):
        GraphicObject.__init__(self, pos, parent=parent)
        HorizontalSpanner.__init__(self, end_x, end_parent)


class TestHorizontalSpanner(unittest.TestCase):
    def setUp(self):
        brown.setup()

    def test_y_mapping_no_parent_outside_flowable(self):
        spanner = MockHorizontalSpanner(Point(Unit(20), Unit(5)), None, Unit(30), None)
        assert spanner.end_parent == spanner
        assert spanner.end_x == Unit(30)
        assert spanner.end_y == Unit(0)
        assert spanner.end_pos == Point(Unit(30), Unit(0))

    def test_y_mapping_with_end_parent_outside_flowable(self):
        end_parent = GraphicObject(Point(Unit(10), Unit(10)))
        spanner = MockHorizontalSpanner(
            Point(Unit(20), Unit(5)), None, Unit(30), end_parent
        )
        assert spanner.end_parent == end_parent
        assert spanner.end_x == Unit(30)
        assert spanner.end_y == Unit(-5)
        assert spanner.end_pos == Point(Unit(30), Unit(-5))

    def test_y_mapping_with_start_and_end_parent_outside_flowable(self):
        start_parent = GraphicObject(Point(Unit(10), Unit(10)))
        end_parent = GraphicObject(Point(Unit(60), Unit(-20)))
        spanner = MockHorizontalSpanner(
            Point(Unit(20), Unit(5)), start_parent, Unit(30), end_parent
        )
        from brown.core.mapping import ancestors

        print(list(ancestors(start_parent)))
        print(list(ancestors(end_parent)))
        assert spanner.end_parent == end_parent
        assert spanner.end_x == Unit(30)
        assert spanner.end_y == Unit(35)
        assert spanner.end_pos == Point(Unit(30), Unit(35))

    def test_y_mapping_no_parent_inside_flowable(self):
        flowable = Flowable(Point(Unit(10), Unit(12)), Unit(10000), Unit(100))
        spanner = MockHorizontalSpanner(
            Point(Unit(20), Unit(5)), flowable, Unit(3000), None
        )
        assert spanner.end_parent == spanner
        assert spanner.end_x == Unit(3000)
        assert spanner.end_y == Unit(0)
        assert spanner.end_pos == Point(Unit(3000), Unit(0))

    def test_y_mapping_with_end_parent_inside_flowable(self):
        flowable = Flowable(Point(Unit(10), Unit(12)), Unit(10000), Unit(100))
        end_parent = GraphicObject(Point(Unit(5000), Unit(10)), parent=flowable)
        spanner = MockHorizontalSpanner(
            Point(Unit(20), Unit(5)), flowable, Unit(3000), end_parent
        )
        assert spanner.end_parent == end_parent
        assert spanner.end_x == Unit(3000)
        assert spanner.end_y == Unit(-5)
        assert spanner.end_pos == Point(Unit(3000), Unit(-5))

    def test_y_mapping_with_start_and_end_parent_inside_flowable(self):
        flowable = Flowable(Point(Unit(10), Unit(12)), Unit(10000), Unit(100))
        start_parent = GraphicObject(Point(Unit(10), Unit(10)), parent=flowable)
        end_parent = GraphicObject(Point(Unit(6000), Unit(-20)), parent=flowable)
        spanner = MockHorizontalSpanner(
            Point(Unit(20), Unit(5)), start_parent, Unit(3000), end_parent
        )
        assert spanner.end_parent == end_parent
        assert spanner.end_x == Unit(3000)
        assert spanner.end_y == Unit(35)
        assert spanner.end_pos == Point(Unit(3000), Unit(35))
