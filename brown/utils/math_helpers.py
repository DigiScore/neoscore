"""Helper functions for simple mathematical calculations"""


from brown.utils.point import Point


def linear_interp(line_start, line_end, x):
    """Calculate the value of a line defined by two points at a given x pos

    Args:
        line_start (Point or tuple): The start of the line
        line_end (Point or tuple): The end of the line
        x (Unit): The position to interpolate from

    Returns: Unit
    """
    line_start = Point(line_start)
    line_end = Point(line_end)
    slope = (line_end.y - line_start.y) / (line_end.x - line_start.x)
    y_intercept = line_start.y - (slope * line_start.x)
    return (slope * x) + y_intercept


def clamp_value(value, minimum, maximum):
    """Clamp a value to fit within a range.

    * If `value` is less than `minimum`, return `minimum`.
    * If `value` is greater than `maximum`, return `maximum`
    * Otherwise, return `value`

    Args:
        value (number or Unit): The value to clamp
        minimum (number or Unit): The lower bound
        maximum (number or Unit): The upper bound

    Returns:
        int or float: The clamped value

    Example:
        >>> clamp_value(-1, 2, 10)
        2
        >>> clamp_value(4.0, 2, 10)
        4.0
        >>> clamp_value(12, 2, 10)
        10
    """
    if value < minimum:
        return minimum
    elif value > maximum:
        return maximum
    else:
        return value
