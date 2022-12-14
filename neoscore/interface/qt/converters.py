"""Helper methods for conversion between ``neoscore.core`` and Qt classes"""

from typing import Union

from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF
from PyQt5.QtGui import QColor, QKeyEvent, QMouseEvent

from neoscore.core.color import Color
from neoscore.core.key_event import KeyEvent, KeyEventType
from neoscore.core.mouse_event import MouseButton, MouseEvent, MouseEventType
from neoscore.core.point import Point
from neoscore.core.rect import Rect
from neoscore.core.units import Unit


def qt_point_to_point(qt_point: Union[QPoint, QPointF]) -> Point:
    """Create a Point from a QPoint or QPointF

    Args:
        qt_point: The source point
    """
    return Point(Unit(qt_point.x()), Unit(qt_point.y()))


def point_to_qt_point(point: Point) -> QPoint:
    """Create a QPoint from a Point

    Args:
        point: The source point
    """
    return QPoint(int(point.x.base_value), int(point.y.base_value))


def point_to_qt_point_f(point: Point) -> QPointF:
    """Create a QPointF from a Point

    Args:
        point: The source point
    """
    return QPointF(point.x.base_value, point.y.base_value)


def qt_rect_to_rect(qt_rect: Union[QRect, QRectF]) -> Rect:
    """Create a Rect from a QRect or QRectF

    Args:
        qt_rect: The source rect
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
        rect: The source rect
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
        rect: The source rect
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
        color: The source ``Color``
    """
    return QColor(color.red, color.green, color.blue, color.alpha)


def q_color_to_color(q_color: QColor) -> Color:
    """Create a ``Color`` from a ``QColor``

    Args:
        q_color: The source ``QColor``
    """
    return Color(q_color.red(), q_color.green(), q_color.blue(), q_color.alpha())


_Q_MOUSE_LEFT_BUTTON = 0x00000001
_Q_MOUSE_RIGHT_BUTTON = 0x00000002
_Q_MOUSE_MIDDLE_BUTTON = 0x00000004


def q_mouse_event_to_mouse_event(
    q_event: QMouseEvent, ns_event_type: MouseEventType, window_pos: QPointF
) -> MouseEvent:
    buttons = int(q_event.buttons())
    if buttons & _Q_MOUSE_LEFT_BUTTON:
        ns_mouse_button = MouseButton.LEFT
    elif buttons & _Q_MOUSE_RIGHT_BUTTON:
        ns_mouse_button = MouseButton.RIGHT
    elif buttons & _Q_MOUSE_MIDDLE_BUTTON:
        ns_mouse_button = MouseButton.MIDDLE
    else:
        ns_mouse_button = None
    q_pos = q_event.windowPos()
    ns_window_pos = (int(q_pos.x()), int(q_pos.y()))
    ns_document_pos = Point(
        Unit(q_pos.x() + window_pos.x()), Unit(q_pos.y() + window_pos.y())
    )
    return MouseEvent(ns_event_type, ns_mouse_button, ns_window_pos, ns_document_pos)


def q_key_event_to_key_event(
    q_event: QKeyEvent, basic_event_type: KeyEventType
) -> KeyEvent:
    resolved_event_type = (
        KeyEventType.AUTO_REPEAT if q_event.isAutoRepeat() else basic_event_type
    )
    return KeyEvent(
        resolved_event_type, q_event.key(), int(q_event.modifiers()), q_event.text()
    )
