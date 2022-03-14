from dataclasses import dataclass
from typing import NamedTuple, Optional

from PyQt5.QtGui import QFont, QPainterPath
from PyQt5.QtWidgets import QGraphicsItem

from neoscore.core import neoscore
from neoscore.interface.font_interface import FontInterface
from neoscore.interface.graphic_object_interface import GraphicObjectInterface
from neoscore.interface.qt.converters import point_to_qt_point_f
from neoscore.interface.qt.q_clipping_path import QClippingPath
from neoscore.utils.units import Unit


class _CachedTextKey(NamedTuple):
    text: str
    family_name: str
    weight: Optional[int]
    italic: bool


class _CachedTextPath(NamedTuple):
    path: QPainterPath
    generation_font_size: float


_PATH_CACHE: dict[_CachedTextKey, _CachedTextPath] = {}

"""TODO LOW We can actually optimize this even further. We can modify
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


@dataclass(frozen=True)
class TextInterface(GraphicObjectInterface):

    """An interface for graphical text objects."""

    text: str

    font: FontInterface

    scale: float = 1

    clip_start_x: Optional[Unit] = None
    """The local starting position of the drawn region in the glyph.

    Use `None` to render from the start
    """

    clip_width: Optional[Unit] = None
    """The width of the visible region.

    Use `None` to render to the end.
    """

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the line to the scene."""
        qt_object = self._create_qt_object()
        neoscore._app_interface.scene.addItem(qt_object)

    def _create_qt_object(self) -> QGraphicsItem:
        """Create and return this interface's underlying Qt object"""
        qt_object = self._get_path(self.text, self.font, self.scale)
        qt_object.setPos(point_to_qt_point_f(self.pos))
        qt_object.setBrush(self.brush.qt_object)
        qt_object.setPen(self.pen.qt_object)
        return qt_object

    ######## PRIVATE METHODS ########

    def _get_path(self, text: str, font: FontInterface, scale: float) -> QClippingPath:
        qt_font = font.qt_object
        needed_font_size = qt_font.pointSizeF()
        key = _CachedTextKey(text, font.family_name, font.weight, font.italic)
        cached_result = _PATH_CACHE.get(key)
        if cached_result:
            cache_scale = needed_font_size / cached_result.generation_font_size
            clipping_path = QClippingPath(
                cached_result.path,
                self.clip_start_x.base_value if self.clip_start_x is not None else 0,
                self.clip_width.base_value if self.clip_width is not None else None,
                cache_scale * scale,
            )
            return clipping_path
        path = TextInterface._create_qt_path(text, qt_font)
        _PATH_CACHE[key] = _CachedTextPath(path, needed_font_size)
        clipping_path = QClippingPath(
            path,
            self.clip_start_x.base_value if self.clip_start_x is not None else 0,
            self.clip_width.base_value if self.clip_width is not None else None,
            scale,
        )
        return clipping_path

    @staticmethod
    def _create_qt_path(text: str, font: QFont) -> QPainterPath:
        qt_path = QPainterPath()
        qt_path.addText(0, 0, font, text)
        return qt_path
