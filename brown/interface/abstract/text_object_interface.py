from abc import ABC


class TextObjectInterface(ABC):
    def __init__(self, x, y, text, font):
        """
        Args:
            x (float): The x position relative to the document
            y (float): The y position relative to the document
            text (str): The text for the object
            font (FontInterface): The font object for the text
        """
        raise NotImplementedError

    @property
    def x(self):
        """float: The x position relative to the document."""
        raise NotImplementedError

    @x.setter
    def x(self, value):
        raise NotImplementedError

    @property
    def y(self):
        """float: The y position relative to the document."""
        raise NotImplementedError

    @y.setter
    def y(self, value):
        raise NotImplementedError

    @property
    def text(self):
        """str: The text for the object"""
        raise NotImplementedError

    @text.setter
    def text(self, value):
        raise NotImplementedError

    @property
    def font(self):
        """ font (FontInterface): The font object for the text """
        raise NotImplementedError

    @font.setter
    def font(self, value):
        raise NotImplementedError

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        raise NotImplementedError
