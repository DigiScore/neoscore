"""Helper methods for conversion between `brown.utils` and Qt classes"""

from typing import Optional, Union

from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF
from PyQt5.QtGui import QColor

from brown.utils.color import Color
from brown.utils.point import Point
from brown.utils.rect import Rect
from brown.utils.units import GraphicUnit, Unit


def qt_point_to_point(
    qt_point: Union[QPoint, QPointF], unit: Optional[Unit] = None
) -> Point:
    """Create a Point from a QPoint or QPointF

    Args:
        qt_point (QPoint or QPointF): The source point
        unit (Unit): An optional unit to convert
            values to in the output `Point`. If omitted, values
            in the output `Point` will be plain `int` or `float` values.

    Returns: Point
    """
    if unit:
        return Point(Unit(qt_point.x()), Unit(qt_point.y()))
    else:
        return Point(qt_point.x(), qt_point.y())


def point_to_qt_point(point: Point) -> QPoint:
    """Create a QPoint from a Point

    Args:
        point (Point): The source point

    Returns: QPoint
    """
    return QPoint(int(point.x.base_value), int(point.y.base_value))


def point_to_qt_point_f(point: Point) -> QPointF:
    """Create a QPointF from a Point

    Args:
        point (Point): The source point

    Returns: QPointF
    """
    return QPointF(point.x.base_value, point.y.base_value)


def qt_rect_to_rect(qt_rect: Union[QRect, QRectF], unit: Optional[Unit] = None) -> Rect:
    """Create a Rect from a QRect or QRectF

    Args:
        qt_rect (QRect or QRectF): The source rect
        unit (Unit): An optional unit to convert
            values to in the output `Rect`. If omitted, values
            in the output `Rect` will be plain `int` or `float` values.

    Returns: Rect
    """
    if unit:
        return Rect(
            qt_rect.x(), qt_rect.y(), qt_rect.width(), qt_rect.height()
        ).in_unit(unit)
    else:
        return Rect(qt_rect.x(), qt_rect.y(), qt_rect.width(), qt_rect.height())


def rect_to_qt_rect(rect: Rect) -> QRect:
    """Create a QRect from a Rect

    Args:
        rect (Rect): The source rect

    Returns: QRect
    """
    return QRect(
        int(rect.x.base_value),
        int(rect.y.base_value),
        int(rect.width.base_value),
        int(rect.height.base_value),
    )


def rect_to_qt_rect_f(rect: Rect) -> QRectF:
    """Create a QRectF from a Rect

    Args:
        rect (Rect): The source rect

    Returns: QRectF
    """
    return QRectF(
        rect.x.base_value,
        rect.y.base_value,
        rect.width.base_value,
        rect.height.base_value,
    )


def color_to_q_color(color: Color) -> QColor:
    """Create a `QColor` from a `Color`

    Args:
        color (Color): The source `Color`

    Returns: QColor
    """
    return QColor(color.red, color.green, color.blue, color.alpha)


def q_color_to_color(q_color: QColor) -> Color:
    """Create a `Color` from a `QColor`

    Args:
        q_color (QColor): The source `QColor`

    Returns: Color
    """
    return Color(q_color.red(), q_color.green(), q_color.blue(), q_color.alpha())
