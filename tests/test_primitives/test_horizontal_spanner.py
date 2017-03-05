import unittest

from brown.core import brown
from brown.core.graphic_object import GraphicObject
from brown.core.flowable_frame import FlowableFrame
from brown.utils.units import Unit
from brown.utils.point import Point
from brown.primitives.horizontal_spanner import HorizontalSpanner


class MockHorizontalSpanner(GraphicObject, HorizontalSpanner):

    """A mock horizontal spanner for testing."""

    def __init__(self, pos, parent, end_x, end_parent):
        """
        Args:
            pos (Point or tuple init args):
            parent (GraphicObject or None):
            end_x (Unit):
            end_parent (GraphicObject or None):
        """
        GraphicObject.__init__(self,
                               pos,
                               parent=parent)
        HorizontalSpanner.__init__(self, end_x, end_parent)


class TestSpanner(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_y_mapping_no_parent_outside_flowable(self):
        spanner = MockHorizontalSpanner(Point(Unit(20), Unit(5)),
                                        None,
                                        Unit(30),
                                        None)
        assert(spanner.end_parent == spanner)
        assert(spanner.end_x == Unit(30))
        assert(spanner.end_y == Unit(0))
        assert(spanner.end_pos == Point(Unit(30), Unit(0)))

    def test_y_mapping_with_end_parent_outside_flowable(self):
        end_parent = GraphicObject(Point(Unit(10), Unit(10)))
        spanner = MockHorizontalSpanner(Point(Unit(20), Unit(5)),
                                        None,
                                        Unit(30),
                                        end_parent)
        assert(spanner.end_parent == end_parent)
        assert(spanner.end_x == Unit(30))
        assert(spanner.end_y == Unit(-5))
        assert(spanner.end_pos == Point(Unit(30), Unit(-5)))

    def test_y_mapping_with_start_and_end_parent_outside_flowable(self):
        start_parent = GraphicObject(Point(Unit(10), Unit(10)))
        end_parent = GraphicObject(Point(Unit(60), Unit(-20)))
        spanner = MockHorizontalSpanner(Point(Unit(20), Unit(5)),
                                        start_parent,
                                        Unit(30),
                                        end_parent)
        assert(spanner.end_parent == end_parent)
        assert(spanner.end_x == Unit(30))
        assert(spanner.end_y == Unit(35))
        assert(spanner.end_pos == Point(Unit(30), Unit(35)))

    def test_y_mapping_no_parent_inside_flowable(self):
        frame = FlowableFrame(Point(Unit(10), Unit(12)),
                              Unit(10000),
                              Unit(100))
        spanner = MockHorizontalSpanner(Point(Unit(20), Unit(5)),
                                        frame,
                                        Unit(3000),
                                        None)
        assert(spanner.end_parent == spanner)
        assert(spanner.end_x == Unit(3000))
        assert(spanner.end_y == Unit(0))
        assert(spanner.end_pos == Point(Unit(3000), Unit(0)))

    def test_y_mapping_with_end_parent_inside_flowable(self):
        frame = FlowableFrame(Point(Unit(10), Unit(12)),
                              Unit(10000),
                              Unit(100))
        end_parent = GraphicObject(Point(Unit(5000), Unit(10)), parent=frame)
        spanner = MockHorizontalSpanner(Point(Unit(20), Unit(5)),
                                        frame,
                                        Unit(3000),
                                        end_parent)
        assert(spanner.end_parent == end_parent)
        assert(spanner.end_x == Unit(3000))
        assert(spanner.end_y == Unit(-5))
        assert(spanner.end_pos == Point(Unit(3000), Unit(-5)))

    def test_y_mapping_with_start_and_end_parent_inside_flowable(self):
        frame = FlowableFrame(Point(Unit(10), Unit(12)),
                              Unit(10000),
                              Unit(100))
        start_parent = GraphicObject(Point(Unit(10), Unit(10)), parent=frame)
        end_parent = GraphicObject(Point(Unit(6000), Unit(-20)), parent=frame)
        spanner = MockHorizontalSpanner(Point(Unit(20), Unit(5)),
                                        start_parent,
                                        Unit(3000),
                                        end_parent)
        assert(spanner.end_parent == end_parent)
        assert(spanner.end_x == Unit(3000))
        assert(spanner.end_y == Unit(35))
        assert(spanner.end_pos == Point(Unit(3000), Unit(35)))
