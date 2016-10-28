from brown.interface.abstract.graphic_object_interface import GraphicObjectInterface


class TextObjectInterface(GraphicObjectInterface):
    def __init__(self, x, y, text, font, parent=None):
        """
        Args:
            x (float): The x position relative to the document
            y (float): The y position relative to the document
            text (str): The text for the object
            font (FontInterface): The font object for the text
            parent: The parent interface object
        """
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
