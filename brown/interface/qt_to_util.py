"""Various helper functions to convert Qt objects to util objects"""


from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF

from brown.utils.rect import Rect
from brown.utils.point import Point
from brown.utils.units import GraphicUnit


def unit_to_qt_int(unit):
    """Create a Qt integer from a Unit

    Args:
        unit (Unit): The source unit

    Returns: int
    """
    return int(GraphicUnit(unit))


def unit_to_qt_float(unit):
    """Create a Qt integer from a Unit

    Args:
        unit (Unit): The source unit

    Returns: float
    """
    return float(GraphicUnit(unit))


def qt_point_to_point(qt_point, unit=None):
    """Create a Point from a QPoint or QPointF

    Args:
        qt_point (QPoint or QPointF): The source point
        unit (Unit): An optional unit to convert
            values to in the output `Point`. If omitted, values
            in the output `Point` will be plain `int` or `float` values.

    Returns: Point
    """
    if unit:
        return Point(qt_point.x(), qt_point.y()).to_unit(unit)
    else:
        return Point(qt_point.x(), qt_point.y())


def point_to_qt_point(point):
    """Create a QPoint from a Point

    Args:
        point (Point): The source point

    Returns: QPoint
    """
    return QPoint(unit_to_qt_int(point.x), unit_to_qt_int(point.y))


def point_to_qt_point_f(point):
    """Create a QPointF from a Point

    Args:
        point (Point): The source point

    Returns: QPointF
    """
    return QPointF(unit_to_qt_float(point.x), unit_to_qt_float(point.y))


def qt_rect_to_rect(qt_rect, unit=None):
    """Create a Rect from a QRect or QRectF

    Args:
        qt_rect (QRect or QRectF): The source rect
        unit (Unit): An optional unit to convert
            values to in the output `Rect`. If omitted, values
            in the output `Rect` will be plain `int` or `float` values.

    Returns: Rect
    """
    if unit:
        return Rect(qt_rect.x(), qt_rect.y(),
                    qt_rect.width(), qt_rect.height()).to_unit(unit)
    else:
        return Rect(qt_rect.x(), qt_rect.y(),
                    qt_rect.width(), qt_rect.height())


def rect_to_qt_rect(rect):
    """Create a QRect from a Rect

    Args:
        rect (Rect): The source rect

    Returns: QRect
    """
    return QRect(unit_to_qt_int(rect.x), unit_to_qt_int(rect.y),
                 unit_to_qt_int(rect.width), unit_to_qt_int(rect.height))


def rect_to_qt_rect_f(rect):
    """Create a QRectF from a Rect

    Args:
        rect (Rect): The source rect

    Returns: QRectF
    """
    return QRectF(unit_to_qt_float(rect.x), unit_to_qt_float(rect.y),
                  unit_to_qt_float(rect.width), unit_to_qt_float(rect.height))
