from brown.utils import math_helpers


def rgb_to_hex(color):
    """
    Convert an ``(r, g, b)`` color tuple to a hexadecimal string.

    Alphabetical characters in the output will be capitalized.

    Args:
        color (tuple): An rgb color tuple of form: (int, int, int)

    Returns: string

    Example:
        >>> rgb_to_hex((0, 0, 0))
        '#000000'
        >>> rgb_to_hex((255, 255, 255))
        '#ffffff'
    """
    return '#{0:02x}{1:02x}{2:02x}'.format(
        math_helpers.clamp_value(int(color[0]), 0, 255),
        math_helpers.clamp_value(int(color[1]), 0, 255),
        math_helpers.clamp_value(int(color[2]), 0, 255))
