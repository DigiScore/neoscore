"""Helper methods for conversion between ``neoscore.core`` and Qt classes"""

from typing import Union

from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF
from PyQt5.QtGui import QColor

from neoscore.core.color import Color
from neoscore.core.point import Point
from neoscore.core.rect import Rect
from neoscore.core.units import Unit


def qt_point_to_point(qt_point: Union[QPoint, QPointF]) -> Point:
    """Create a Point from a QPoint or QPointF

    Args:
        qt_point: The source point

    Returns: Point
    """
    return Point(Unit(qt_point.x()), Unit(qt_point.y()))


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


def qt_rect_to_rect(qt_rect: Union[QRect, QRectF]) -> Rect:
    """Create a Rect from a QRect or QRectF

    Args:
        qt_rect (QRect or QRectF): The source rect

    Returns: Rect
    """
    return Rect(
        Unit(qt_rect.x()),
        Unit(qt_rect.y()),
        Unit(qt_rect.width()),
        Unit(qt_rect.height()),
    )


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
    """Create a ``QColor`` from a ``Color``

    Args:
        color (Color): The source ``Color``

    Returns: QColor
    """
    return QColor(color.red, color.green, color.blue, color.alpha)


def q_color_to_color(q_color: QColor) -> Color:
    """Create a ``Color`` from a ``QColor``

    Args:
        q_color (QColor): The source ``QColor``

    Returns: Color
    """
    return Color(q_color.red(), q_color.green(), q_color.blue(), q_color.alpha())
