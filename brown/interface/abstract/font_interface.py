from abc import ABC


class FontInterface(ABC):
    def __init__(self, family_name, size, weight=1, italic=False):
        """
        Args:
            family_name (str): The name of the font family
            size (float): The size of the font, in pixels
            weight (int): The font weight
            italic (bool): Italicized or not
        """
        raise NotImplementedError

    ######## PUBLIC PROPERTIES ########

    @property
    def ascent(self):
        raise NotImplementedError

    @property
    def ascent(self):
        raise NotImplementedError
