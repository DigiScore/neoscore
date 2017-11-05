from brown.core import brown
from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.interface.qt.converters import point_to_qt_point_f
from brown.interface.qt.q_enhanced_text_item import QEnhancedTextItem
from brown.utils.point import Point


class TextInterface(GraphicObjectInterface):

    """An interface for graphical text objects."""

    def __init__(self, brown_object, pos, text, font, brush,
                 origin_offset=None, scale_factor=1, clip_start_x=None,
                 clip_width=None):
        """
        Args:
            brown_object (Text): The brown object this belongs to
            pos (Point[GraphicUnit] or tuple): The position of the path root
                relative to the document.
            text (str): The text for the object
            font (FontInterface): The font object for the text
            brush (BrushInterface): The brush for the object.
            scale_factor (float): A hard scaling factor.
            clip_start_x (Unit or None): The local starting position for the
                clipping region. Use `None` to render from the start.
            clip_width (Unit or None): The width of the clipping region.
                Use `None` to render to the end
        """
        super().__init__(brown_object)
        if origin_offset:
            self._origin_offset = origin_offset
        else:
            self._origin_offset = Point(0, 0)
        self._scale_factor = scale_factor
        self._text = text
        self.clip_start_x = clip_start_x
        self.clip_width = clip_width
        self.qt_object = QEnhancedTextItem(
            self.text,
            origin_offset=point_to_qt_point_f(self.origin_offset),
            scale_factor=self.scale_factor,
            clip_start_x=self.clip_start_x,
            clip_width=self.clip_width)
        # Let setters trigger Qt setters for attributes not in constructor
        self.font = font
        self.pos = pos
        self.brush = brush
        self.update_geometry()

    ######## PUBLIC PROPERTIES ########

    @property
    def text(self):
        """str: The text for the object"""
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.qt_object.setText(value)

    @property
    def font(self):
        """FontInterface: The font object for the text """
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        self.qt_object.setFont(value.qt_object)

    @property
    def origin_offset(self):
        """Point: A hard offset to be applied to the rendered text"""
        return self._origin_offset

    @origin_offset.setter
    def origin_offset(self, value):
        self._origin_offset = value
        self.qt_object._origin_offset = self._origin_offset

    @property
    def scale_factor(self):
        """float: A hard scale factor to be applied to the rendered text"""
        return self._scale_factor

    @scale_factor.setter
    def scale_factor(self, value):
        self._scale_factor = value
        self.qt_object._scale_factor = self._scale_factor

    ######## PUBLIC METHODS ########

    def update_geometry(self):
        self.qt_object.update_geometry()

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        brown._app_interface.scene.addItem(self.qt_object)
