from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.brush import Brush, SimpleBrushDef, brush_from_simple_def
from neoscore.core.pen import Pen, SimplePenDef, pen_from_simple_def
from neoscore.core.positioned_object import PositionedObject
from neoscore.utils.point import PointDef

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class PaintedObject(PositionedObject):
    """A PositionedObject which is painted with a pen (outline) and brush (fill)."""

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[Parent] = None,
        brush: Optional[SimpleBrushDef] = None,
        pen: Optional[SimplePenDef] = None,
    ):
        """
        Args:
            pos: The position of the object relative to its parent
            pen: The pen to draw outlines
        with.
            brush: The brush to fill shapes with.
            parent: The parent object or None
        """
        super().__init__(pos, parent)
        self.pen = pen
        self.brush = brush
        self._children: list[PositionedObject] = []

    ######## PUBLIC PROPERTIES ########

    @property
    def pen(self) -> Pen:
        """The pen to draw outlines with"""
        return self._pen

    @pen.setter
    def pen(self, value: SimplePenDef):
        if value:
            self._pen = pen_from_simple_def(value)
        else:
            self._pen = Pen()

    @property
    def brush(self) -> Brush:
        """The brush to draw outlines with

        As a convenience, this may be set with a hex color string
        for a solid color brush of that color. For brushes using
        alpha channels and non-solid-color fill patterns, a fully
        initialized brush must be passed to this.
        """
        return self._brush

    @brush.setter
    def brush(self, value: SimpleBrushDef):
        if value:
            self._brush = brush_from_simple_def(value)
            if isinstance(value, str):
                self._brush = Brush(value)
            elif isinstance(value, Brush):
                self._brush = value
            else:
                raise TypeError
        else:
            self._brush = Brush()
