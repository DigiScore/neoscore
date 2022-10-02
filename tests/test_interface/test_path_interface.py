from neoscore.core.brush_pattern import BrushPattern
from neoscore.core.color import Color
from neoscore.core.pen_cap_style import PenCapStyle
from neoscore.core.pen_join_style import PenJoinStyle
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.point import ORIGIN
from neoscore.core.units import Unit
from neoscore.interface.brush_interface import BrushInterface
from neoscore.interface.path_interface import (
    PathInterface,
    ResolvedCurveTo,
    ResolvedLineTo,
    ResolvedMoveTo,
)
from neoscore.interface.pen_interface import PenInterface

from ..helpers import AppTest


class TestPathInterface(AppTest):
    def setUp(self):
        super().setUp()
        self.pen = PenInterface(
            Color("#000000"),
            Unit(0),
            PenPattern.SOLID,
            PenJoinStyle.BEVEL,
            PenCapStyle.SQUARE,
        )
        self.brush = BrushInterface(Color("#000000"), BrushPattern.SOLID)

    def test_rotation(self):
        path = PathInterface(ORIGIN, None, 1, 0, ORIGIN, self.brush, self.pen, [])
        assert path._create_qt_object().rotation() == 0
        path = PathInterface(ORIGIN, None, 1, 20, ORIGIN, self.brush, self.pen, [])
        assert path._create_qt_object().rotation() == 20

    def test_create_qt_path_with_move(self):
        qt_path = PathInterface.create_qt_path([ResolvedMoveTo(Unit(10), Unit(12))])
        assert qt_path.elementCount() == 1
        el_0 = qt_path.elementAt(0)
        assert el_0.isMoveTo()
        assert el_0.x == 10
        assert el_0.y == 12
        assert qt_path.currentPosition().x() == 10
        assert qt_path.currentPosition().y() == 12

    def test_create_qt_path_with_line(self):
        qt_path = PathInterface.create_qt_path([ResolvedLineTo(Unit(10), Unit(12))])
        assert qt_path.elementCount() == 2
        # Note how an initial line-to implicitly adds a move-to at the origin
        el_0 = qt_path.elementAt(0)
        assert el_0.isMoveTo()
        assert el_0.x == 0
        assert el_0.y == 0
        el_1 = qt_path.elementAt(1)
        assert el_1.isLineTo()
        assert el_1.x == 10
        assert el_1.y == 12
        assert qt_path.currentPosition().x() == 10
        assert qt_path.currentPosition().y() == 12

    def test_create_qt_path_with_cubic(self):
        """This test also helps document some poorly-documented
        quirks in Qt path construction.

        ``QPainterPath::ElementType`` is ambiguous in differentiating
        between curve control points and curve end points. They are
        stored sequentially in the path element list; the first
        element in the sequence is a ``CurveToElement``, all following
        elements in the curve are ``CurveToDataElement``. Despite this,
        all elements until the last in the sequence are control
        points; the final element is the curve end point.

        For instance, if a cubic line is drawn with two control points
        - ``cubicTo(0, 1, 2, 3, 4, 5)`` - they are stored in the Qt
        element list as `[<CurveToElement, 0, 1>, <CurveToDataElement,
        2, 3>, <CurveToDataElement, 4, 5>]` where the first two are
        control points and the last is the end point.

        """
        qt_path = PathInterface.create_qt_path(
            [ResolvedCurveTo(Unit(1), Unit(2), Unit(3), Unit(4), Unit(5), Unit(6))]
        )
        assert qt_path.elementCount() == 4
        # Note how an initial curve-to implicitly adds a move-to at the origin
        el_0 = qt_path.elementAt(0)
        assert el_0.isMoveTo()
        assert el_0.x == 0
        assert el_0.y == 0
        el_1 = qt_path.elementAt(1)
        assert el_1.isCurveTo()
        assert el_1.x == 1
        assert el_1.y == 2
        el_2 = qt_path.elementAt(2)
        # QPainterPath::CurveToDataElement == 3
        # (Qt provides no boolean check method for these)
        assert el_2.type == 3
        assert el_2.x == 3
        assert el_2.y == 4
        el_3 = qt_path.elementAt(3)
        assert el_3.type == 3
        assert el_3.x == 5
        assert el_3.y == 6
        assert qt_path.currentPosition().x() == 5
        assert qt_path.currentPosition().y() == 6
