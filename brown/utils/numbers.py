def clamp_value(value, minimum, maximum):
    """Clamp a value to fit within a range.

    * If `value` is less than `minimum`, return `minimum`.
    * If `value` is greater than `maximum`, return `maximum`
    * Otherwise, return `value`

    Args:
        value (int or float): The value to clamp
        minimum (int or float): The lower bound
        maximum (int or float): The upper bound

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
