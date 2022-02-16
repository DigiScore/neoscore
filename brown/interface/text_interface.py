from typing import Dict, NamedTuple, Optional

from PyQt5.QtGui import QFont, QPainterPath

from brown.core import brown
from brown.interface.font_interface import FontInterface
from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.interface.qt.converters import point_to_qt_point_f
from brown.interface.qt.q_clipping_path import QClippingPath
from brown.interface.qt.q_enhanced_text_item import QEnhancedTextItem
from brown.utils.point import Point
from brown.utils.units import GraphicUnit


class _CachedTextKey(NamedTuple):
    text: str
    family_name: str
    weight: Optional[int]
    italic: bool


class _CachedTextPath(NamedTuple):
    path: QPainterPath
    generation_font_size: float


_PATH_CACHE: Dict[_CachedTextKey, _CachedTextPath] = {}


class TextInterface(GraphicObjectInterface):

    """An interface for graphical text objects."""

    def __init__(
        self,
        brown_object,
        pos,
        text,
        font,
        brush,
        origin_offset=None,
        scale_factor=1,
        clip_start_x=None,
        clip_width=None,
    ):
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
        # if origin_offset:
        #     self._origin_offset = origin_offset
        # else:
        #     self._origin_offset = Point(0, 0)
        # self._scale_factor = scale_factor
        self._text = text
        self.clip_start_x = clip_start_x
        self.clip_width = clip_width
        self.qt_object = self._get_path(text, font)
        # Let setters trigger Qt setters for attributes not in constructor
        self.pos = pos
        self.brush = brush
        # self.update_geometry()

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

    # def update_geometry(self):
    #     self.qt_object.update_geometry()

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        brown._app_interface.scene.addItem(self.qt_object)

    ######## PRIVATE METHODS ########

    def _get_path(self, text: str, font: FontInterface):
        qt_font = font.qt_object
        needed_font_size = qt_font.pointSizeF()
        key = _CachedTextKey(text, font.family_name, font.weight, font.italic)
        cached_result = _PATH_CACHE.get(key)
        if cached_result:
            scale = needed_font_size / cached_result.generation_font_size
            return QClippingPath(
                cached_result.path, self.clip_start_x, self.clip_width, scale
            )
        path = TextInterface._create_qt_path(text, qt_font)
        _PATH_CACHE[key] = _CachedTextPath(path, needed_font_size)
        return QClippingPath(path, self.clip_start_x, self.clip_width, 1)

    @staticmethod
    def _create_qt_path(text: str, font: QFont) -> QPainterPath:
        qt_path = QPainterPath()
        qt_path.addText(0, 0, font, text)
        return qt_path
