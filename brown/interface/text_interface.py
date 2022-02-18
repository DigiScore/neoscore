from typing import Dict, NamedTuple, Optional

from PyQt5.QtGui import QFont, QPainterPath, QPen

from brown.core import brown
from brown.interface.font_interface import FontInterface
from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.interface.qt.converters import point_to_qt_point_f
from brown.interface.qt.q_clipping_path import QClippingPath
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

"""TODO We can actually optimize this even further. We can modify
q_clipping_path so it explicitly stores paint results in the global
QPixmapCache. If this were specialized to just text items, the cache
key would be like _CachedTextKey, except it also includes font size
and scale. This would allow us to not only cache the paths being sent
to Qt objects, but the rendered pixmaps themselves. This would be very
efficient for us because so many constructed path objects are
identical. Furthermore, if I manage to move the runtime to the OpenGL
system, I believe these rendered pixmaps would reside directly in GPU
memory.

see https://doc.qt.io/qt-5/qgraphicsitem.html#setCacheMode
"""


class TextInterface(GraphicObjectInterface):

    """An interface for graphical text objects."""

    def __init__(
        self,
        pos,
        text,
        font,
        brush,
        scale=1,
        clip_start_x=None,
        clip_width=None,
    ):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the path root
                relative to the document.
            text (str): The text for the object
            font (FontInterface): The font object for the text
            brush (BrushInterface): The brush for the object.
            scale (float): A hard scaling factor.
            clip_start_x (Unit or None): The local starting position for the
                clipping region. Use `None` to render from the start.
            clip_width (Unit or None): The width of the clipping region.
                Use `None` to render to the end
        """
        super().__init__()
        self._text = text
        self.clip_start_x = clip_start_x
        self.clip_width = clip_width
        self._scale = scale
        self.qt_object = self._get_path(text, font, scale)
        # Let setters trigger Qt setters for attributes not in constructor
        self.pos = pos
        self.brush = brush
        # TODO support setting pen on text objects
        self.qt_object.setPen(QPen(0))  # No pen

    ######## PUBLIC PROPERTIES ########

    @property
    def text(self):
        """str: The text for the object"""
        return self._text

    @property
    def scale(self):
        """float: A hard scale factor to be applied to the rendered text"""
        return self._scale

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        brown._app_interface.scene.addItem(self.qt_object)

    ######## PRIVATE METHODS ########

    def _get_path(self, text: str, font: FontInterface, additional_scale: float):
        qt_font = font.qt_object
        needed_font_size = qt_font.pointSizeF()
        key = _CachedTextKey(text, font.family_name, font.weight, font.italic)
        cached_result = _PATH_CACHE.get(key)
        if cached_result:
            cache_scale = needed_font_size / cached_result.generation_font_size
            clipping_path = QClippingPath(
                cached_result.path, self.clip_start_x, self.clip_width
            )
            clipping_path.setScale(cache_scale * additional_scale)
            return clipping_path
        path = TextInterface._create_qt_path(text, qt_font)
        _PATH_CACHE[key] = _CachedTextPath(path, needed_font_size)
        clipping_path = QClippingPath(path, self.clip_start_x, self.clip_width)
        clipping_path.setScale(additional_scale)
        return clipping_path

    @staticmethod
    def _create_qt_path(text: str, font: QFont) -> QPainterPath:
        qt_path = QPainterPath()
        qt_path.addText(0, 0, font, text)
        return qt_path
