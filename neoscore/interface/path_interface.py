from dataclasses import dataclass
from typing import NamedTuple, Optional, Union

from PyQt5.QtGui import QPainterPath

from neoscore.core import neoscore
from neoscore.interface.graphic_object_interface import GraphicObjectInterface
from neoscore.interface.qt.converters import point_to_qt_point_f
from neoscore.interface.qt.q_clipping_path import QClippingPath
from neoscore.utils.units import Unit


class ResolvedMoveTo(NamedTuple):
    x: Unit
    y: Unit


class ResolvedLineTo(NamedTuple):
    x: Unit
    y: Unit


class ResolvedCurveTo(NamedTuple):
    c1_x: Unit
    c1_y: Unit
    c2_x: Unit
    c2_y: Unit
    end_x: Unit
    end_y: Unit


ResolvedPathElement = Union[ResolvedMoveTo, ResolvedLineTo, ResolvedCurveTo]
"""A path element whose position is relative to its path"""


@dataclass(frozen=True)
class PathInterface(GraphicObjectInterface):
    """Interface for a generic graphic path object."""

    elements: list[ResolvedPathElement]

    clip_start_x: Optional[Unit] = None
    """The local starting position of the drawn region in the glyph.

    Use `None` to render from the start
    """

    clip_width: Optional[Unit] = None
    """The width of the visible region.

    Use `None` to render to the end.
    """

    ######## Public Methods ########

    @staticmethod
    def create_qt_path(elements: list[ResolvedPathElement]) -> QPainterPath:
        path = QPainterPath()
        for el in elements:
            if isinstance(el, ResolvedLineTo):
                path.lineTo(el.x.base_value, el.y.base_value)
            elif isinstance(el, ResolvedMoveTo):
                path.moveTo(el.x.base_value, el.y.base_value)
            elif isinstance(el, ResolvedCurveTo):
                path.cubicTo(
                    el.c1_x.base_value,
                    el.c1_y.base_value,
                    el.c2_x.base_value,
                    el.c2_y.base_value,
                    el.end_x.base_value,
                    el.end_y.base_value,
                )
            else:
                raise TypeError("Unknown ResolvedPathElement type")
        return path

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        qt_object = self._create_qt_object()
        neoscore._app_interface.scene.addItem(qt_object)

    ######## PRIVATE METHODS ########

    def _create_qt_object(self):
        painter_path = PathInterface.create_qt_path(self.elements)
        qt_object = QClippingPath(
            painter_path,
            self.clip_start_x.base_value if self.clip_start_x is not None else None,
            self.clip_width.base_value if self.clip_width is not None else None,
        )
        qt_object.setPos(point_to_qt_point_f(self.pos))
        qt_object.setBrush(self.brush.qt_object)
        qt_object.setPen(self.pen.qt_object)  # No pen
        qt_object.update_geometry()
        return qt_object
