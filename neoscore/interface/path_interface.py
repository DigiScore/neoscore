from __future__ import annotations

from dataclasses import dataclass
from typing import List, NamedTuple, Optional, Union

from PyQt5.QtGui import QPainterPath
from typing_extensions import TypeAlias

from neoscore.core.units import Unit
from neoscore.interface.brush_interface import BrushInterface
from neoscore.interface.pen_interface import PenInterface
from neoscore.interface.positioned_object_interface import PositionedObjectInterface
from neoscore.interface.qt.converters import point_to_qt_point_f
from neoscore.interface.qt.q_clipping_path import QClippingPath


class ResolvedMoveTo(NamedTuple):
    """A canvas-space move-to element."""

    # Add blank docstrings to suppress ugly default namedtuple docstring used by Sphinx
    x: Unit
    """"""
    y: Unit
    """"""


class ResolvedLineTo(NamedTuple):
    """A canvas-space line-to element."""

    x: Unit
    """"""
    y: Unit
    """"""


class ResolvedCurveTo(NamedTuple):
    """A canvas-space curve-to element."""

    c1_x: Unit
    """"""
    c1_y: Unit
    """"""
    c2_x: Unit
    """"""
    c2_y: Unit
    """"""
    end_x: Unit
    """"""
    end_y: Unit
    """"""


ResolvedPathElement: TypeAlias = Union[ResolvedMoveTo, ResolvedLineTo, ResolvedCurveTo]
"""A path element whose position is relative to its path"""


@dataclass(frozen=True)
class PathInterface(PositionedObjectInterface):
    """Interface for a generic graphic path object."""

    brush: BrushInterface

    pen: PenInterface

    elements: List[ResolvedPathElement]

    background_brush: Optional[BrushInterface] = None

    clip_start_x: Optional[Unit] = None
    """The local starting position of the drawn region in the glyph.

    Use ``None`` to render from the start
    """

    clip_width: Optional[Unit] = None
    """The width of the visible region.

    Use ``None`` to render to the end.
    """

    @staticmethod
    def create_qt_path(elements: List[ResolvedPathElement]) -> QPainterPath:
        path = QPainterPath()
        path.setFillRule(1)

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
        """Render the path to the scene."""
        self._register_qt_object(self._create_qt_object())

    def _create_qt_object(self) -> QClippingPath:
        painter_path = PathInterface.create_qt_path(self.elements)
        qt_object = QClippingPath(
            painter_path,
            self.clip_start_x.base_value if self.clip_start_x is not None else 0,
            self.clip_width.base_value if self.clip_width is not None else None,
            self.scale,
            self.rotation,
            self.background_brush.qt_object if self.background_brush else None,
            defer_geometry_calculation=True,
            transform_origin=point_to_qt_point_f(self.transform_origin),
        )
        qt_object.setPos(point_to_qt_point_f(self.pos))
        qt_object.setBrush(self.brush.qt_object)
        qt_object.setPen(self.pen.qt_object)
        qt_object.update_geometry()
        return qt_object
