from brown.interface.text_object_interface import TextObjectInterface
from brown.core import brown
from brown.core.graphic_object import GraphicObject


class TextObject(GraphicObject):

    _interface_class = TextObjectInterface

    def __init__(self, pos, text, font=None, parent=None, scale_factor=1):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the path root
                relative to the document.
            text (str): The text to be displayed
            font (Font): The font for the object.
            parent (GraphicObject): The parent (core-level) object or None
            scale_factor(float): A hard scaling factor.
        """

        self._interface = None
        if font:
            self.font = font
        else:
            self.font = brown.text_font
        self.text = text
        self.scale_factor = scale_factor
        super().__init__(pos, parent=parent)

    ######## PUBLIC PROPERTIES ########

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError
        else:
            self._text = value
            if self._interface:
                self._interface.text = value

    @property
    def font(self):
        """Font: The text font"""
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        if self._interface:
            self._interface.font = value._interface

    @property
    def scale_factor(self):
        """float: A hard scale factor to be applied to the rendered text"""
        return self._scale_factor

    @scale_factor.setter
    def scale_factor(self, value):
        self._scale_factor = value

    ######## PRIVATE PROPERTIES ########

    @property
    def _origin_offset(self):
        """The origin offset override for this object."""
        return None

    ######## PRIVATE METHODS ########

    def _render_complete(self, pos):
        """Render the entire object.

        Args:
            pos (Point): The rendering position in document space for drawing.

        Returns: None
        """
        self._interface = self._interface_class(
            pos,
            self.text,
            self.font._interface,
            origin_offset=self._origin_offset,
            scale_factor=self.scale_factor
        )
        self._interface.render()
