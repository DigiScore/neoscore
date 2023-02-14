import math

import pytest

from neoscore.core.brush import Brush
from neoscore.core.path import Path
from neoscore.core.path_element import ControlPoint, CurveTo, LineTo, MoveTo
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Mm, Unit
from neoscore.interface.path_interface import (
    ResolvedCurveTo,
    ResolvedLineTo,
    ResolvedMoveTo,
)

from ..helpers import AppTest, assert_path_els_equal


class TestPath(AppTest):
    def setUp(self):
        super().setUp()
        self.brush = Brush("#ff0000")
        self.pen = Pen("#00ff00")

    def test_init(self):
        mock_parent = PositionedObject(ORIGIN, parent=None)
        path = Path((Unit(5), Unit(6)), mock_parent, self.brush, self.pen)
        assert path.pos == Point(Unit(5), Unit(6))
        assert path.pen == self.pen
        assert path.brush == self.brush
        assert path.background_brush is None

    def test_background_brush(self):
        bg_brush = Brush("#ff0000")
        obj = Path((Unit(5), Unit(6)), None, background_brush=bg_brush)
        assert obj.background_brush == bg_brush
        obj.background_brush = "#00ffff"
        assert obj.background_brush == Brush("#00ffff")

    def test_rotation(self):
        path = Path(ORIGIN, None)
        assert path.rotation == 0
        path.rotation = 20
        assert path.rotation == 20
        assert Path(ORIGIN, None, rotation=123).rotation == 123

    def test_transform_origin_setter(self):
        path = Path(ORIGIN, None)
        assert path.transform_origin == ORIGIN
        path.transform_origin = (Unit(12), Unit(12))
        assert path.transform_origin == Point(Unit(12), Unit(12))
        assert Path(
            ORIGIN, None, transform_origin=(Unit(12), Unit(12))
        ).transform_origin == (Unit(12), Unit(12))

    def test_straight_line(self):
        path = Path.straight_line((Unit(5), Unit(6)), None, (Unit(10), Unit(11)))
        assert path.pos == Point(Unit(5), Unit(6))
        assert len(path.elements) == 2
        assert_path_els_equal(path.elements[0], MoveTo(ORIGIN, path))
        assert_path_els_equal(path.elements[1], LineTo(Point(Unit(10), Unit(11)), path))

    def test_straight_line_with_parent_end(self):
        start_parent = PositionedObject((Unit(50), Unit(60)), None)
        end_parent = PositionedObject((Unit(500), Unit(600)), None)
        path = Path.straight_line(
            (Unit(5), Unit(5)), start_parent, (Unit(10), Unit(10)), end_parent
        )
        assert path.pos == Point(Unit(5), Unit(5))
        assert len(path.elements) == 2
        assert_path_els_equal(path.elements[0], MoveTo(ORIGIN, path))
        assert_path_els_equal(
            path.elements[1], LineTo(Point(Unit(10), Unit(10)), end_parent)
        )

    def test_line_to(self):
        path = Path((Unit(5), Unit(6)), None)
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
        path = Path((Unit(5), Unit(6)), None)
        parent = PositionedObject((Unit(100), Unit(50)), None)
        path.line_to(Unit(1), Unit(3), parent)
        assert path.elements[-1].parent == parent
        resolved_els = path._resolve_path_elements()
        assert resolved_els == [
            ResolvedMoveTo(ZERO, ZERO),
            ResolvedLineTo(Unit(100 + 1 - 5), Unit(50 + 3 - 6)),
        ]

    def test_cubic_to_with_no_parents(self):
        path = Path((Unit(5), Unit(6)), None)
        path.cubic_to(Unit(10), Unit(11), ZERO, Unit(1), Unit(5), Unit(6))
        assert len(path.elements) == 2
        assert_path_els_equal(path.elements[0], MoveTo(ORIGIN, path))
        assert_path_els_equal(
            path.elements[1],
            CurveTo(
                Point(Unit(5), Unit(6)),
                path,
                ControlPoint(Point(Unit(10), Unit(11)), path),
                ControlPoint(Point(ZERO, Unit(1)), path),
            ),
        )
        resolved_els = path._resolve_path_elements()
        assert resolved_els == [
            ResolvedMoveTo(ZERO, ZERO),
            ResolvedCurveTo(Unit(10), Unit(11), ZERO, Unit(1), Unit(5), Unit(6)),
        ]

    def test_cubic_to_with_parents(self):
        path = Path((Unit(100), Unit(200)), None)
        parent_1 = PositionedObject((Unit(10), Unit(20)), None)
        parent_2 = PositionedObject((Unit(30), Unit(40)), None)
        parent_3 = PositionedObject((Unit(50), Unit(60)), None)
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
                Point(Unit(5), Unit(6)),
                parent_3,
                ControlPoint(Point(Unit(1), Unit(2)), parent_1),
                ControlPoint(Point(Unit(3), Unit(4)), parent_2),
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
        path = Path((Unit(5), Unit(6)), None)
        path.move_to(Unit(10), Unit(11))
        assert len(path.elements) == 1
        assert_path_els_equal(path.elements[0], MoveTo(Point(Unit(10), Unit(11)), path))

    def test_move_to_with_parent(self):
        path = Path(ORIGIN, None)
        parent = PositionedObject((Unit(100), Unit(50)), None)
        path.move_to(Unit(10), Unit(11), parent)
        assert len(path.elements) == 1
        assert_path_els_equal(
            path.elements[0], MoveTo(Point(Unit(10), Unit(11)), parent)
        )

    def test_close_subpath(self):
        path = Path((Unit(5), Unit(6)), None)
        path.line_to(Unit(10), Unit(10))
        path.line_to(Unit(10), Unit(100))
        path.close_subpath()
        assert len(path.elements) == 4
        assert_path_els_equal(path.elements[3], LineTo(ORIGIN, path))

    def test_close_subpath_with_move_to(self):
        path = Path((Unit(5), Unit(6)), None)
        path.line_to(Unit(10), Unit(10))
        path.move_to(Unit(100), Unit(100))
        path.line_to(Unit(10), Unit(100))
        path.close_subpath()
        assert len(path.elements) == 5
        assert_path_els_equal(
            path.elements[4], LineTo(Point(Unit(100), Unit(100)), path)
        )

    def test_close_subpath_with_move_to_and_new_parent(self):
        start_parent = Path((Unit(5), Unit(6)), None)
        end_parent = Path((Unit(50), Unit(60)), None)
        start_parent.line_to(Unit(10), Unit(10))
        start_parent.move_to(Unit(100), Unit(100), end_parent)
        start_parent.line_to(Unit(10), Unit(100))
        start_parent.close_subpath()
        assert len(start_parent.elements) == 5
        assert_path_els_equal(
            start_parent.elements[4], LineTo(Point(Unit(100), Unit(100)), end_parent)
        )

    def test_rect(self):
        path = Path.rect(ORIGIN, None, Unit(5), Unit(6), self.brush, self.pen)
        assert path.brush == self.brush
        assert path.pen == self.pen
        assert_path_els_equal(
            path.elements,
            [
                MoveTo(ORIGIN, path),
                LineTo((Unit(5), ZERO), path),
                LineTo((Unit(5), Unit(6)), path),
                LineTo((ZERO, Unit(6)), path),
                LineTo(ORIGIN, path),
            ],
        )

    def test_ellipse(self):
        path = Path.ellipse(
            (Mm(1), Mm(2)), None, Unit(5), Unit(6), self.brush, self.pen
        )
        assert path.brush == self.brush
        assert path.pen == self.pen
        # These values were visually verified and copied here
        assert_path_els_equal(
            path.elements,
            [
                MoveTo((Unit(0.0), Unit(3.0)), path),
                CurveTo(
                    (Unit(2.5), Unit(0.0)),
                    path,
                    ControlPoint((Unit(0.0), Unit(1.343)), path),
                    ControlPoint((Unit(1.119), Unit(0.0)), path),
                ),
                CurveTo(
                    (Unit(5.0), Unit(3.0)),
                    path,
                    ControlPoint((Unit(3.881), Unit(0.0)), path),
                    ControlPoint((Unit(5.0), Unit(1.343)), path),
                ),
                CurveTo(
                    (Unit(2.5), Unit(6.0)),
                    path,
                    ControlPoint((Unit(5.0), Unit(4.657)), path),
                    ControlPoint((Unit(3.881), Unit(6.0)), path),
                ),
                CurveTo(
                    (Unit(0.0), Unit(3.0)),
                    path,
                    ControlPoint((Unit(1.119), Unit(6.0)), path),
                    ControlPoint((Unit(0.0), Unit(4.657)), path),
                ),
            ],
            3,
        )

    def test_ellipse_from_center(self):
        path = Path.ellipse_from_center(
            (Mm(1), Mm(2)), None, Unit(5), Unit(6), self.brush, self.pen
        )
        assert path.brush == self.brush
        assert path.pen == self.pen
        expected = Path.ellipse((Unit(-2.5), Unit(-3)), None, Unit(5), Unit(6))
        for actual, expected in zip(path.elements, expected.elements):
            assert_path_els_equal(actual, expected, 3, compare_parents=False)

    def test_arc(self):
        path = Path.arc(
            ORIGIN,
            None,
            Unit(5),
            Unit(6),
            math.pi / 4,
            math.pi * 1.5,
            self.brush,
            self.pen,
        )
        assert path.brush == self.brush
        assert path.pen == self.pen
        assert_path_els_equal(
            path.elements,
            [
                MoveTo(Point(Unit(4.4205531), Unit(4.920553)), path),
                CurveTo(
                    Point(Unit(0.899539), Unit(5.30466)),
                    path,
                    ControlPoint(Point(Unit(3.5366429), Unit(6.1933)), path),
                    ControlPoint(Point(Unit(1.960231), Unit(6.365356)), path),
                ),
                CurveTo(
                    Point(Unit(0.5794468), Unit(1.0794468)),
                    path,
                    ControlPoint(Point(Unit(-0.1611532), Unit(4.2439)), path),
                    ControlPoint(Point(Unit(-0.30446), Unit(2.352277)), path),
                ),
                CurveTo(
                    Point(Unit(2.5), Unit(0.0)),
                    path,
                    ControlPoint(Point(Unit(1.05443), Unit(0.39546)), path),
                    ControlPoint(Point(Unit(1.75805), Unit(0)), path),
                ),
            ],
            3,
        )

    def test_arc_with_invalid_angle(self):
        with pytest.raises(ValueError):
            Path.arc(ORIGIN, None, Unit(10), Unit(10), 1.0, 1.0 + 2 * math.pi)

        with pytest.raises(ValueError):
            Path.arc(ORIGIN, None, Unit(10), Unit(10), 1.0, 1.0)

        with pytest.raises(ValueError):
            Path.arc(ORIGIN, None, Unit(10), Unit(10), 0, 2 * math.pi)

    def test_arrow_without_end_parent(self):
        path = Path.arrow(
            (Unit(10), Unit(11)),
            None,
            (Unit(5), Unit(6)),
            brush=self.brush,
            pen=self.pen,
        )
        assert path.brush == self.brush
        assert path.pen == self.pen
        assert_path_els_equal(
            path.elements,
            [
                MoveTo(Point(Unit(0.0), Unit(0.0)), path),
                LineTo(Point(Unit(-0.381086), Unit(0.3175719)), path),
                LineTo(Point(Unit(0.0821713), Unit(0.8734812)), path),
                LineTo(Point(Unit(-1.1699), Unit(1.91693)), path),
                LineTo(Point(Unit(5.0), Unit(6.0)), path),
                LineTo(Point(Unit(2.09648), Unit(-0.80511)), path),
                LineTo(Point(Unit(0.8443), Unit(0.23833)), path),
                LineTo(Point(Unit(0.3810), Unit(-0.3175)), path),
                LineTo(Point(Unit(0.0), Unit(0.0)), path),
            ],
            2,
        )

    def test_arrow_with_end_parent(self):
        start_parent = PositionedObject((Unit(100), Unit(200)), None)
        end_parent = PositionedObject((Unit(1000), Unit(2000)), None)
        path = Path.arrow(
            (Unit(10), Unit(11)),
            start_parent,
            (Unit(5), Unit(6)),
            end_parent,
            self.brush,
            self.pen,
        )
        assert path.brush == self.brush
        assert path.pen == self.pen
        assert_path_els_equal(
            path.elements,
            [
                MoveTo(Point(Unit(0.0), Unit(0.0)), path),
                LineTo(Point(Unit(-0.44393), Unit(0.22135)), path),
                LineTo(Point(Unit(891.3938), Unit(1788.87935)), path),
                LineTo(Point(Unit(889.93523), Unit(1789.606656)), path),
                LineTo(Point(Unit(895.0), Unit(1795.0)), path),
                LineTo(Point(Unit(893.74043), Unit(1787.709357)), path),
                LineTo(Point(Unit(892.2817), Unit(1788.4366)), path),
                LineTo(Point(Unit(0.44393), Unit(-0.22135)), path),
                LineTo(Point(Unit(0.0), Unit(0.0)), path),
            ],
            2,
        )
