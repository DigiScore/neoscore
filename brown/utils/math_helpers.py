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
