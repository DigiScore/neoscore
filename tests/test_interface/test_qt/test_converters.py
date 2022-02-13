from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF

from brown.interface.qt.converters import (
    point_to_qt_point,
    point_to_qt_point_f,
    qt_point_to_point,
    qt_rect_to_rect,
    rect_to_qt_rect,
    rect_to_qt_rect_f,
)
from brown.utils.point import Point
from brown.utils.rect import Rect
from brown.utils.units import GraphicUnit

# qt_point_to_point ###########################################################


def test_qt_point_to_point_with_q_point():
    point = qt_point_to_point(QPoint(1, 2))
    assert isinstance(point, Point)
    assert point.x == GraphicUnit(1)
    assert point.y == GraphicUnit(2)


def test_qt_point_to_point_with_q_point_f():
    point = qt_point_to_point(QPointF(1.5, 2.5))
    assert isinstance(point, Point)
    assert point.x == GraphicUnit(1.5)
    assert point.y == GraphicUnit(2.5)


def test_qt_point_to_point_with_q_point_and_unit_class():
    point = qt_point_to_point(QPoint(1, 2), GraphicUnit)
    assert isinstance(point, Point)
    assert point.x == GraphicUnit(1)
    assert point.y == GraphicUnit(2)


def test_qt_point_to_point_with_q_point_f_and_unit_class():
    point = qt_point_to_point(QPointF(1.5, 2.5), GraphicUnit)
    assert isinstance(point, Point)
    assert point.x == GraphicUnit(1.5)
    assert point.y == GraphicUnit(2.5)


# point_to_qt_point ###########################################################


def test_point_to_qt_point():
    qpoint = point_to_qt_point(Point(GraphicUnit(1.2), GraphicUnit(2.2)))
    assert isinstance(qpoint, QPoint)
    assert qpoint.x() == 1
    assert qpoint.y() == 2


# point_to_qt_point_f #########################################################


def test_point_to_qt_point_f():
    qpoint = point_to_qt_point_f(Point(GraphicUnit(1.2), GraphicUnit(2.2)))
    assert isinstance(qpoint, QPointF)
    assert qpoint.x() == 1.2
    assert qpoint.y() == 2.2


# qt_rect_to_point ############################################################


def test_qt_rect_to_rect_with_q_rect():
    rect = qt_rect_to_rect(QRect(1, 2, 3, 4))
    assert isinstance(rect, Rect)
    assert rect.x == 1
    assert rect.y == 2
    assert rect.width == 3
    assert rect.height == 4


def test_qt_rect_to_rect_with_q_rect_f():
    rect = qt_rect_to_rect(QRectF(1.5, 2.5, 3.5, 4.5))
    assert isinstance(rect, Rect)
    assert rect.x == 1.5
    assert rect.y == 2.5
    assert rect.width == 3.5
    assert rect.height == 4.5


def test_qt_rect_to_rect_with_q_rect_and_unit_class():
    rect = qt_rect_to_rect(QRect(1, 2, 3, 4), GraphicUnit)
    assert isinstance(rect, Rect)
    assert rect.x == GraphicUnit(1)
    assert rect.y == GraphicUnit(2)
    assert rect.width == GraphicUnit(3)
    assert rect.height == GraphicUnit(4)


def test_qt_rect_to_rect_with_q_rect_f_and_unit_class():
    rect = qt_rect_to_rect(QRectF(1.5, 2.5, 3.5, 4.5), GraphicUnit)
    assert isinstance(rect, Rect)
    assert rect.x == GraphicUnit(1.5)
    assert rect.y == GraphicUnit(2.5)
    assert rect.width == GraphicUnit(3.5)
    assert rect.height == GraphicUnit(4.5)


# rect_to_qt_rect #############################################################


def test_rect_to_qt_rect():
    qrect = rect_to_qt_rect(
        Rect(GraphicUnit(1.2), GraphicUnit(2.2), GraphicUnit(3.2), GraphicUnit(4.2))
    )
    assert isinstance(qrect, QRect)
    assert qrect.x() == 1
    assert qrect.y() == 2
    assert qrect.width() == 3
    assert qrect.height() == 4


# rect_to_qt_rect_f ###########################################################


def test_rect_to_qt_rect_f():
    qrect = rect_to_qt_rect_f(
        Rect(GraphicUnit(1.2), GraphicUnit(2.2), GraphicUnit(3.2), GraphicUnit(4.2))
    )
    assert isinstance(qrect, QRectF)
    assert qrect.x() == 1.2
    assert qrect.y() == 2.2
    assert qrect.width() == 3.2
    assert qrect.height() == 4.2
