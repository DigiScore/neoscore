import unittest

from brown.core import brown
from brown.core.brush import Brush
from brown.core.invisible_object import InvisibleObject
from brown.core.path import Path
from brown.core.path_element import ControlPoint, CurveTo, LineTo, MoveTo
from brown.core.pen import Pen
from brown.interface.path_interface import (
    ResolvedCurveTo,
    ResolvedLineTo,
    ResolvedMoveTo,
)
from brown.utils.point import ORIGIN, Point
from brown.utils.units import ZERO, Unit

from ..helpers import assert_path_els_equal


class TestPath(unittest.TestCase):
    def setUp(self):
        brown.setup()

    def test_init(self):
        mock_parent = InvisibleObject(ORIGIN, parent=None)
        test_pen = Pen("#eeeeee")
        test_brush = Brush("#dddddd")
        path = Path((Unit(5), Unit(6)), test_pen, test_brush, mock_parent)
        assert path.pos == Point(Unit(5), Unit(6))
        assert path.pen == test_pen
        assert path.brush == test_brush

    def test_straight_line(self):
        path = Path.straight_line((Unit(5), Unit(6)), (Unit(10), Unit(11)))
        assert path.pos == Point(Unit(5), Unit(6))
        assert len(path.elements) == 2
        assert_path_els_equal(path.elements[0], MoveTo(ORIGIN, path))
        assert_path_els_equal(path.elements[1], LineTo(Point(Unit(10), Unit(11)), path))

    def test_line_to(self):
        path = Path((Unit(5), Unit(6)))
        path.line_to(Unit(10), Unit(12))
        assert len(path.elements) == 2
        assert_path_els_equal(path.elements[0], MoveTo(ORIGIN, path))
        assert_path_els_equal(path.elements[1], LineTo(Point(Unit(10), Unit(12)), path))
        resolved_els = path._resolve_path_elements()
        assert resolved_els == [
            ResolvedMoveTo(ZERO, ZERO),
            ResolvedLineTo(Unit(10), Unit(12)),
        ]

    def test_line_to_with_parent(self):
        path = Path((Unit(5), Unit(6)))
        parent = InvisibleObject((Unit(100), Unit(50)))
        path.line_to(Unit(1), Unit(3), parent)
        assert path.elements[-1].parent == parent
        resolved_els = path._resolve_path_elements()
        assert resolved_els == [
            ResolvedMoveTo(ZERO, ZERO),
            ResolvedLineTo(Unit(100 + 1 - 5), Unit(50 + 3 - 6)),
        ]

    def test_cubic_to_with_no_parents(self):
        path = Path((Unit(5), Unit(6)))
        path.cubic_to(Unit(10), Unit(11), ZERO, Unit(1), Unit(5), Unit(6))
        assert len(path.elements) == 2
        assert_path_els_equal(path.elements[0], MoveTo(ORIGIN, path))
        assert_path_els_equal(
            path.elements[1],
            CurveTo(
                ControlPoint(Point(Unit(10), Unit(11)), path),
                ControlPoint(Point(ZERO, Unit(1)), path),
                Point(Unit(5), Unit(6)),
                path,
            ),
        )
        resolved_els = path._resolve_path_elements()
        assert resolved_els == [
            ResolvedMoveTo(ZERO, ZERO),
            ResolvedCurveTo(Unit(10), Unit(11), ZERO, Unit(1), Unit(5), Unit(6)),
        ]

    def test_cubic_to_with_parents(self):
        path = Path((Unit(Unit(100)), Unit(Unit(200))))
        parent_1 = InvisibleObject((Unit(Unit(10)), Unit(Unit(20))))
        parent_2 = InvisibleObject((Unit(Unit(30)), Unit(Unit(40))))
        parent_3 = InvisibleObject((Unit(Unit(50)), Unit(Unit(60))))
        path.cubic_to(
            Unit(1),
            Unit(2),
            Unit(3),
            Unit(4),
            Unit(5),
            Unit(6),
            parent_1,
            parent_2,
            parent_3,
        )
        assert len(path.elements) == 2
        assert_path_els_equal(path.elements[0], MoveTo(ORIGIN, path))
        assert_path_els_equal(
            path.elements[1],
            CurveTo(
                ControlPoint(Point(Unit(1), Unit(2)), parent_1),
                ControlPoint(Point(Unit(3), Unit(4)), parent_2),
                Point(Unit(5), Unit(6)),
                parent_3,
            ),
        )
        resolved_els = path._resolve_path_elements()
        assert resolved_els == [
            ResolvedMoveTo(ZERO, ZERO),
            ResolvedCurveTo(
                Unit(10 + 1 - 100),
                Unit(20 + 2 - 200),
                Unit(30 + 3 - 100),
                Unit(40 + 4 - 200),
                Unit(50 + 5 - 100),
                Unit(60 + 6 - 200),
            ),
        ]

    def test_move_to_with_no_parent(self):
        path = Path((Unit(5), Unit(6)))
        path.move_to(Unit(10), Unit(11))
        assert len(path.elements) == 1
        assert_path_els_equal(path.elements[0], MoveTo(Point(Unit(10), Unit(11)), path))

    def test_move_to_with_parent(self):
        path = Path(ORIGIN)
        parent = InvisibleObject((Unit(100), Unit(50)))
        path.move_to(Unit(10), Unit(11), parent)
        assert len(path.elements) == 1
        assert_path_els_equal(
            path.elements[0], MoveTo(Point(Unit(10), Unit(11)), parent)
        )

    def test_close_subpath(self):
        path = Path((Unit(5), Unit(6)))
        path.line_to(Unit(10), Unit(10))
        path.line_to(Unit(10), Unit(100))
        path.close_subpath()
        assert len(path.elements) == 4
        assert_path_els_equal(path.elements[3], MoveTo(ORIGIN, path))
