from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


from brown.core import brown
from brown.interface.abstract.text_object_interface import TextObjectInterface
from brown.utils import color


class TextObjectInterfaceQt(TextObjectInterface):
    def __init__(self, x, y, text, font):
        """
        Args:
            x (float): The x position relative to the document
            y (float): The y position relative to the document
            text (str): The text for the object
            font (FontInterface): The font object for the text
        """
        self.text = text
        self.font = font
        self._qt_object = QtWidgets.QGraphicsTextItem(self.text)
        self._qt_object.setFont(self.font._qt_object)
        self.x = x
        self.y = y

    ######## PUBLIC PROPERTIES ########

    @property
    def x(self):
        """float: The x position relative to the document."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._qt_object.setX(self._x)

    @property
    def y(self):
        """float: The y position relative to the document."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._qt_object.setY(self._y)

    @property
    def default_color(self):
        """str: A hexadecimal color controlling the color of unformatted text.

        If this is set to an RGB tuple it will be converted to and stored
        in hexadecimal form

        By default this value is black ('#000000')
        """
        return self._default_color

    @default_color.setter
    def default_color(self, value):
        if isinstance(value, tuple):
            if len(value) == 3:
                self._default_color = color.rgb_to_hex(value)
            else:
                raise ValueError(
                    'RGB tuple for BrushInterface[Qt] must be len 3')
        elif isinstance(value, str):
            self._default_color = value
        elif value is None:
            self._qt_object.setDefaultTextColor(QtGui.QColor('#000000'))
        else:
            raise TypeError
        self._qt_object.setDefaultTextColor(QtGui.QColor(self._default_color))

    @property
    def text(self):
        """str: The text for the object"""
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise ValueError
        else:
            self._text = value

    @property
    def font(self):
        """ font (FontInterface): The font object for the text """
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        # TODO: Propogate font change to qt object

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        brown._app_interface.scene.addItem(self._qt_object)
