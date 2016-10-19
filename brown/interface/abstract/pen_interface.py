from abc import ABC


class PenInterface(ABC):
    """Interface for a generic drawing pen controlling path outline appearance.

    Currently only solid colors are supported.
    """

    def __init__(self, color):
        """
        Args:
            color (str or tuple): Either a hexadecimal color string or a
                3-tuple of RGB int's
        """
        raise NotImplementedError

    ######## PUBLIC PROPERTIES ########

    @property
    def color(self):
        """str: A hexadecimal color string value.

        If this is set to an RGB tuple it will be converted to and stored
        in hexadecimal form
        """
        raise NotImplementedError

    @color.setter
    def color(self, value):
        raise NotImplementedError
