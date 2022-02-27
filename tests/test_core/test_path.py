import unittest

import pytest

from brown.core import brown
from brown.core.brush import Brush
from brown.core.invisible_object import InvisibleObject
from brown.core.path import Path
from brown.core.path_element import ControlPoint, CurveTo, LineTo, MoveTo, PathElement
from brown.core.pen import Pen
from brown.utils.point import ORIGIN, Point
from brown.utils.units import ZERO, Unit


class TestPath(unittest.TestCase):
    def setUp(self):
        brown.setup()

    def test_init(self):
        mock_parent = InvisibleObject((Unit(0), Unit(0)), parent=None)
        test_pen = Pen("#eeeeee")
        test_brush = Brush("#dddddd")
        path = Path((Unit(5), Unit(6)), test_pen, test_brush, mock_parent)
        assert path.pos == Point(Unit(5), Unit(6))
        assert path.pen == test_pen
        assert path.brush == test_brush

    def test_straight_line(self):
        test_line = Path.straight_line((Unit(5), Unit(6)), (Unit(10), Unit(11)))
        assert test_line.pos == Point(Unit(5), Unit(6))
        assert len(test_line.elements) == 2
        assert test_line.elements[0] == MoveTo(ORIGIN, test_line)
        assert test_line.elements[1] == LineTo(Point(Unit(10), Unit(11)), test_line)

    def test_line_to(self):
        path = Path((Unit(5), Unit(6)))
        path.line_to(Unit(10), Unit(12))
        assert len(path.elements) == 2
        assert path.elements[0] == MoveTo(ORIGIN, path)
        assert path.elements[1].pos == Point(Unit(10), Unit(12))

    def test_line_to_with_parent(self):
        path = Path((Unit(5), Unit(6)))
        parent = InvisibleObject((Unit(100), Unit(50)))
        path.line_to(Unit(1), Unit(3), parent)
        assert path.elements[-1].parent == parent

    def test_cubic_to_with_no_parents(self):
        path = Path((Unit(5), Unit(6)))
        path.cubic_to(Unit(10), Unit(11), Unit(0), Unit(1), Unit(5), Unit(6))
        assert len(path.elements) == 2
        assert path.elements[0] == MoveTo(ORIGIN, path)
        assert path.elements[1] == CurveTo(
            Point(Unit(5), Unit(6)),
            path,
            ControlPoint(Point(Unit(10), Unit(11)), path),
            ControlPoint(Point(Unit(0), Unit(1)), path),
        )

    def test_cubic_to_with_parents(self):
        path = Path((Unit(Unit(0)), Unit(Unit(0))))
        parent_1 = InvisibleObject((Unit(Unit(100)), Unit(Unit(50))))
        parent_2 = InvisibleObject((Unit(Unit(100)), Unit(Unit(50))))
        parent_3 = InvisibleObject((Unit(Unit(100)), Unit(Unit(50))))
        path.cubic_to(
            Unit(10),
            Unit(11),
            Unit(0),
            Unit(1),
            Unit(5),
            Unit(6),
            parent_1,
            parent_2,
            parent_3,
        )
        assert len(path.elements) == 2
        assert path.elements[0] == MoveTo(ORIGIN, path)
        assert path.elements[1] == CurveTo(
            Point(Unit(5), Unit(6)),
            parent_3,
            ControlPoint(Point(Unit(10), Unit(11)), parent_1),
            ControlPoint(Point(Unit(0), Unit(1)), parent_2),
        )

    def test_move_to_with_no_parent(self):
        path = Path((Unit(5), Unit(6)))
        path.move_to(Unit(10), Unit(11))
        assert len(path.elements) == 1
        assert path.elements[0] == MoveTo(Point(Unit(10), Unit(11)), path)

    def test_move_to_with_parent(self):
        path = Path((Unit(0), Unit(0)))
        parent = InvisibleObject((Unit(100), Unit(50)))
        path.move_to(Unit(10), Unit(11), parent)
        assert len(path.elements) == 1
        assert path.elements[0] == MoveTo(Point(Unit(10), Unit(11)), parent)

    def test_close_subpath(self):
        path = Path((Unit(5), Unit(6)))
        path.line_to(Unit(10), Unit(10))
        path.line_to(Unit(10), Unit(100))
        path.close_subpath()
        assert len(path.elements) == 4
        assert path.elements[3] == MoveTo(ORIGIN, path)
