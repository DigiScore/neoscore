from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF

from neoscore.core.point import Point
from neoscore.core.rect import Rect
from neoscore.core.units import Unit
from neoscore.interface.qt.converters import (
    point_to_qt_point,
    point_to_qt_point_f,
    qt_point_to_point,
    qt_rect_to_rect,
    rect_to_qt_rect,
    rect_to_qt_rect_f,
)

# qt_point_to_point ###########################################################


def test_qt_point_to_point_with_q_point():
    point = qt_point_to_point(QPoint(1, 2))
    assert isinstance(point, Point)
    assert point.x == Unit(1)
    assert point.y == Unit(2)


def test_qt_point_to_point_with_q_point_f():
    point = qt_point_to_point(QPointF(1.5, 2.5))
    assert isinstance(point, Point)
    assert point.x == Unit(1.5)
    assert point.y == Unit(2.5)


# point_to_qt_point ###########################################################


def test_point_to_qt_point():
    qpoint = point_to_qt_point(Point(Unit(1.2), Unit(2.2)))
    assert isinstance(qpoint, QPoint)
    assert qpoint.x() == 1
    assert qpoint.y() == 2


# point_to_qt_point_f #########################################################


def test_point_to_qt_point_f():
    qpoint = point_to_qt_point_f(Point(Unit(1.2), Unit(2.2)))
    assert isinstance(qpoint, QPointF)
    assert qpoint.x() == 1.2
    assert qpoint.y() == 2.2


# qt_rect_to_point ############################################################


def test_qt_rect_to_rect_with_q_rect():
    rect = qt_rect_to_rect(QRect(1, 2, 3, 4))
    assert isinstance(rect, Rect)
    assert rect.x == Unit(1)
    assert rect.y == Unit(2)
    assert rect.width == Unit(3)
    assert rect.height == Unit(4)


def test_qt_rect_to_rect_with_q_rect_f():
    rect = qt_rect_to_rect(QRectF(1.5, 2.5, 3.5, 4.5))
    assert isinstance(rect, Rect)
    assert rect.x == Unit(1.5)
    assert rect.y == Unit(2.5)
    assert rect.width == Unit(3.5)
    assert rect.height == Unit(4.5)


# rect_to_qt_rect #############################################################


def test_rect_to_qt_rect():
    qrect = rect_to_qt_rect(Rect(Unit(1.2), Unit(2.2), Unit(3.2), Unit(4.2)))
    assert isinstance(qrect, QRect)
    assert qrect.x() == 1
    assert qrect.y() == 2
    assert qrect.width() == 3
    assert qrect.height() == 4


# rect_to_qt_rect_f ###########################################################


def test_rect_to_qt_rect_f():
    qrect = rect_to_qt_rect_f(Rect(Unit(1.2), Unit(2.2), Unit(3.2), Unit(4.2)))
    assert isinstance(qrect, QRectF)
    assert qrect.x() == 1.2
    assert qrect.y() == 2.2
    assert qrect.width() == 3.2
    assert qrect.height() == 4.2
