"""A module containing interoperable units"""

"""






Probably won't end up completing or using -
too much API mental overhead for end users to be
worth it. Better to provide simple scalar conversion
factors so users can convert units themselves in a
less implicit way.





"""

import pytest


from brown.config import config



class BaseUnit:
    """A base class for custom units"""

    ######## SPECIAL METHODS ########



    # ...

    ######## PUBLIC METHODS ########

    @property
    def val(self):
        return self._val



class Pixel(BaseUnit):

    def __init__(self, val):
        if isinstance(val, (int, float)):
            self._val = val
        elif isinstance(val, Inch):
            self._val = _inch_to_pixel(inch_val)
        else:
            raise TypeError

    ######## PRIVATE METHODS ########

    @staticmethod
    def _any_to_pixel(inch_val):
        """Convert an inch value to a pixel value.

        Args:
            inch_val (int or float): Value of inches

        Returns: int or float: Value in pixels
        """
        return config.PRINT_PPI * inch_val



class Inch:

    def __init__(self, val):
        if isinstance(val, (int, float)):
            self._val = val
        elif isinstance(val, Inch):
            self._val = config.PRINT_PPI * val
        else:
            raise TypeError



def _convert_units(value, target_type):
    """Take a typed unit value and return its float/int value for a target type

    Args:
        value (Any): The input typed unit value
        target_type (BaseUnit subclass): The target type to retrieve the value in

    Returns:
        int or float: Value as it would be expressed in `target_type` units

    Example:
        >>> inches = Inch(3)
        >>> _convert_units(inches, Pixel)  # Assuming config.PRINT_PPI == 300  # doctest: +SKIP
        900
    """
    # Convert to pixel values as intermediary
    # Special case to save some time
    if type(value) == target_type:
        return value.val
    # Find ratios from all types to pixels
    int_to_pix = 1
    float_to_pix = 1
    inch_to_pix = config.PRINT_PPI
    pix_to_pix = 1
