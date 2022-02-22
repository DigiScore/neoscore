import unittest

import pytest

from brown.core import brown
from brown.core.brush import Brush
from brown.core.invisible_object import InvisibleObject
from brown.core.path import Path
from brown.core.path_element_type import PathElementType
from brown.core.pen import Pen
from brown.utils.point import Point
from brown.utils.units import GraphicUnit, Unit


class TestPath(unittest.TestCase):
    def setUp(self):
        brown.setup()

    def test_init(self):
        mock_parent = InvisibleObject((Unit(0), Unit(0)), parent=None)
        test_pen = Pen("#eeeeee")
        test_brush = Brush("#dddddd")
        path = Path((Unit(5), Unit(6)), test_pen, test_brush, mock_parent)
        assert isinstance(path.pos, Point)
        assert path.x == GraphicUnit(5)
        assert path.y == GraphicUnit(6)
        assert isinstance(path.current_draw_pos, Point)
        assert path.current_draw_pos == Point(GraphicUnit(0), GraphicUnit(0))
        assert path.pen == test_pen
        assert path.brush == test_brush

    def test_straight_line(self):
        test_line = Path.straight_line((Unit(5), Unit(6)), (Unit(10), Unit(11)))
        assert isinstance(test_line.pos, Point)
        assert test_line.x == GraphicUnit(5)
        assert test_line.y == GraphicUnit(6)
        assert test_line.current_draw_pos == Point(GraphicUnit(10), GraphicUnit(11))

    # noinspection PyPropertyAccess
    def test_current_path_pos_has_no_setter(self):
        test_line = Path((Unit(0), Unit(0)))
        with pytest.raises(AttributeError):
            test_line.current_draw_pos = (7, 8)

    def test_line_to(self):
        path = Path((Unit(5), Unit(6)))
        path.line_to(Unit(10), Unit(12))
        assert len(path.elements) == 2
        assert path.elements[-1].pos.x == GraphicUnit(10)
        assert path.current_draw_pos == Point(GraphicUnit(10), GraphicUnit(12))

    def test_line_to_with_parent(self):
        path = Path((Unit(5), Unit(6)))
        parent = InvisibleObject((Unit(100), Unit(50)))
        path.line_to(Unit(1), Unit(3), parent)
        assert path.elements[-1].parent == parent

    def test_cubic_to_with_no_parents(self):
        path = Path((Unit(5), Unit(6)))
        path.cubic_to(Unit(10), Unit(11), Unit(0), Unit(1), Unit(5), Unit(6))
        assert len(path.elements) == 4
        assert path.elements[0].element_type == PathElementType.move_to
        assert path.elements[0].pos == Point(GraphicUnit(0), GraphicUnit(0))
        assert path.elements[1].element_type == PathElementType.control_point
        assert path.elements[1].pos == Point(Unit(10), Unit(11))
        assert path.elements[2].element_type == PathElementType.control_point
        assert path.elements[2].pos == Point(Unit(0), Unit(1))
        assert path.elements[3].element_type == PathElementType.curve_to
        assert path.elements[3].pos == Point(Unit(5), Unit(6))
        assert path.current_draw_pos == Point(GraphicUnit(5), GraphicUnit(6))

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
        assert len(path.elements) == 4
        assert path.elements[0].element_type == PathElementType.move_to
        assert path.elements[0].pos == Point(GraphicUnit(0), GraphicUnit(0))
        assert path.elements[1].element_type == PathElementType.control_point
        assert path.elements[1].pos == Point(Unit(10), Unit(11))
        assert path.elements[1].parent == parent_1
        assert path.elements[2].element_type == PathElementType.control_point
        assert path.elements[2].pos == Point(Unit(0), Unit(1))
        assert path.elements[2].parent == parent_2
        assert path.elements[3].element_type == PathElementType.curve_to
        assert path.elements[3].pos == Point(Unit(5), Unit(6))
        assert path.elements[3].parent == parent_3
        assert path.current_draw_pos == Point(GraphicUnit(105), GraphicUnit(56))

    def test_move_to_with_no_parent(self):
        path = Path((Unit(5), Unit(6)))
        path.move_to(Unit(10), Unit(11))
        assert len(path.elements) == 1
        assert path.elements[0].element_type == PathElementType.move_to
        assert path.elements[0].pos == Point(Unit(10), Unit(11))
        assert path.current_draw_pos == Point(GraphicUnit(10), GraphicUnit(11))

    def test_move_to_with_parent(self):
        path = Path((Unit(0), Unit(0)))
        parent = InvisibleObject((Unit(100), Unit(50)))
        path.move_to(Unit(10), Unit(11), parent)
        assert len(path.elements) == 1
        assert path.elements[0].element_type == PathElementType.move_to
        assert path.elements[0].pos == Point(Unit(10), Unit(11))
        assert path.elements[0].parent == parent
        assert path.current_draw_pos == Point(GraphicUnit(110), GraphicUnit(61))

    def test_close_subpath(self):
        path = Path((Unit(5), Unit(6)))
        path.line_to(Unit(10), Unit(10))
        path.line_to(Unit(10), Unit(100))
        path.close_subpath()
        assert len(path.elements) == 4
        assert path.elements[3].element_type == PathElementType.move_to
        assert path.elements[3].pos == Point(GraphicUnit(0), GraphicUnit(0))
        assert path.current_draw_pos == Point(GraphicUnit(0), GraphicUnit(0))
