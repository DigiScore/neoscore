from __future__ import annotations

from typing import Optional

from neoscore.core.brush import Brush, BrushDef
from neoscore.core.pen import Pen, PenDef
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject


class PaintedObject(PositionedObject):
    """A ``PositionedObject`` which is painted with a pen (outline) and brush (fill).

    This is mostly meant to be used as a superclass for other classes which need this
    behavior.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """
        Args:
            pos: The position of the object relative to its parent
            pen: The pen to draw outlines with.
            brush: The brush to fill shapes with.
            parent: The parent object or None
        """
        super().__init__(pos, parent)
        self.pen = pen
        self.brush = brush
        self._children: List[PositionedObject] = []

    @property
    def pen(self) -> Pen:
        """The pen to draw outlines with"""
        return self._pen

    @pen.setter
    def pen(self, value: PenDef):
        if value:
            self._pen = Pen.from_def(value)
        else:
            self._pen = Pen()

    @property
    def brush(self) -> Brush:
        """The brush to draw outlines with.

        As a convenience, this may be set with a hex color string for a solid color
        brush of that color. For brushes using alpha channels and non-solid-color fill
        patterns, a fully initialized brush must be passed to this.
        """
        return self._brush

    @brush.setter
    def brush(self, value: BrushDef):
        if value:
            self._brush = Brush.from_def(value)
        else:
            self._brush = Brush()
