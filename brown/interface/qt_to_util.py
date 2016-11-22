"""Various helper functions to convert Qt objects to util objects"""


from brown.utils.rect import Rect
from brown.utils.point import Point


def qt_point_to_point(qt_point, unit=None):
    """Create a Point from a QPoint or QPointF

    Args:
        qt_point (QPoint or QPointF): The source point
        unit (BaseUnit): An optional unit to convert
            values to in the output `Point`. If omitted, values
            in the output `Point` will be plain `int` or `float` values.

    Returns: Point
    """
    if unit:
        return Point.with_unit(qt_point.x(), qt_point.y(),
                               unit=unit)
    else:
        return Point(qt_point.x(), qt_point.y())


def qt_rect_to_rect(qt_rect, unit=None):
    """Create a Rect from a QRect or QRectF

    Args:
        qt_rect (QRect or QRectF): The source rect
        unit (BaseUnit): An optional unit to convert
            values to in the output `Rect`. If omitted, values
            in the output `Rect` will be plain `int` or `float` values.

    Returns: Rect
    """
    if unit:
        return Rect.with_unit(qt_rect.x(), qt_rect.y(),
                              qt_rect.width(), qt_rect.height(),
                              unit)
    else:
        return Rect(qt_rect.x(), qt_rect.y(),
                    qt_rect.width(), qt_rect.height())
