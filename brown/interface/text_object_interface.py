from brown.core import brown
from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.interface.qt_ext.q_enhanced_text_item import QEnhancedTextItem
from brown.interface.qt_to_util import point_to_qt_point_f
from brown.utils.point import Point


class TextObjectInterface(GraphicObjectInterface):

    _interface_class = QEnhancedTextItem

    def __init__(self,
                 pos,
                 text,
                 font,
                 origin_offset=None,
                 scale_factor=1,
                 clip_start_x=None,
                 clip_width=None):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the path root
                relative to the document.
            text (str): The text for the object
            font (FontInterface): The font object for the text
            scale_factor (float): A hard scaling factor.
            clip_start_x (Unit or None): The local starting position for the
                clipping region. Use `None` to render from the start.
            clip_width (Unit or None): The width of the clipping region.
                Use `None` to render to the end
        """
        if origin_offset:
            self._origin_offset = origin_offset
        else:
            self._origin_offset = Point(0, 0)
        self._scale_factor = scale_factor
        self._text = text
        self.clip_start_x = clip_start_x
        self.clip_width = clip_width
        self._qt_object = self._interface_class(
            self.text,
            origin_offset=point_to_qt_point_f(self.origin_offset),
            scale_factor=self.scale_factor,
            clip_start_x=self.clip_start_x,
            clip_width=self.clip_width)
        # Let setters trigger Qt setters for attributes not in constructor
        self.font = font
        self.pos = Point(pos)


    ######## PUBLIC PROPERTIES ########

    @property
    def text(self):
        """str: The text for the object"""
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._qt_object.setText(value)

    @property
    def font(self):
        """FontInterface: The font object for the text """
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        self._qt_object.setFont(value._qt_object)

    @property
    def origin_offset(self):
        """Point: A hard offset to be applied to the rendered text"""
        return self._origin_offset

    @origin_offset.setter
    def origin_offset(self, value):
        self._origin_offset = value
        self._qt_object._origin_offset = self._origin_offset

    @property
    def scale_factor(self):
        """float: A hard scale factor to be applied to the rendered text"""
        return self._scale_factor

    @scale_factor.setter
    def scale_factor(self, value):
        self._scale_factor = value
        self._qt_object._scale_factor = self._scale_factor

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        brown._app_interface.scene.addItem(self._qt_object)
