import unittest

from brown.core import brown
from brown.core.graphic_object import GraphicObject
from brown.core.spanner import Spanner
from brown.utils.point import Point
from brown.utils.units import Unit


class MockSpanner(GraphicObject, Spanner):

    """A mock spanner for testing."""

    def __init__(self, pos, parent, end_pos, end_parent):
        """
        Args:
            pos (Point or tuple init args):
            parent (GraphicObject or None):
            end_pos (Point or tuple init args):
            end_parent (GraphicObject or None):
        """
        GraphicObject.__init__(self,
                               pos,
                               parent=parent)
        Spanner.__init__(self, end_pos, end_parent)


class TestSpanner(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_inputs_converted_to_parent_points(self):
        spanner = MockSpanner((Unit(0), Unit(1)),
                              None,
                              (Unit(2), Unit(3)),
                              None)
        assert(spanner.end_pos == Point(Unit(2), Unit(3)))
        assert(spanner.end_parent == spanner)

    def test_length_no_parents(self):
        spanner = MockSpanner((Unit(1), Unit(2)),
                              brown.document.pages[0],
                              (Unit(5), Unit(7)),
                              brown.document.pages[0])
        # math.sqrt(((5-1)**2) + ((7-2)**2))
        self.assertAlmostEqual(Unit(spanner.spanner_length).value,
                               6.4031242374328485)

    def test_length_with_self_parent(self):
        parent = MockSpanner((Unit(1), Unit(2)),
                             None,
                             (Unit(0), Unit(0)),
                             None)
        spanner = MockSpanner((Unit(3), Unit(7)),
                              parent,
                              (Unit(4), Unit(5)),
                              None)
        # math.sqrt((4**2) + (5**2))
        self.assertAlmostEqual(Unit(spanner.spanner_length).value,
                               6.4031242374328485)

    def test_length_with_parents(self):
        parent_1 = MockSpanner((Unit(1), Unit(2)),
                               None,
                              (Unit(0), Unit(0)),
                               None)
        parent_2 = MockSpanner((Unit(11), Unit(12)),
                               None,
                              (Unit(0), Unit(0)),
                               None)
        spanner = MockSpanner((Unit(1), Unit(2)),
                              parent_1,
                              (Unit(4), Unit(5)),
                              parent_2)
        # math.sqrt(((15-2)**2) + ((17-4)**2))
        self.assertAlmostEqual(Unit(spanner.spanner_length).value,
                               18.384776310850235)
