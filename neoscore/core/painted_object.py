from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.brush import (
    DEFAULT_BRUSH,
    Brush,
    SimpleBrushDef,
    brush_from_simple_def,
)
from neoscore.core.pen import DEFAULT_PEN, Pen, SimplePenDef, pen_from_simple_def
from neoscore.core.positioned_object import PositionedObject
from neoscore.utils.point import PointDef

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


# TODO HIGH update docstrings between PaintedObject and PositionedObject


class PaintedObject(PositionedObject):
    """An abstract graphic object.

    All classes in `core` which have the ability to be displayed
    should be subclasses of this.

    A single GraphicObject can have multiple graphical representations,
    calculated at render-time. If the object's ancestor is a Flowable,
    it will be rendered as a flowable object, capable of being wrapped around
    lines.

    The position of this object is relative to that of its parent.
    Each GraphicObject has another GraphicObject for a parent, except
    `Page` objects, whose parent is always the global `Document`.

    For convenience, the parent may be initialized to None to indicate
    the first page of the document.

    To place objects directly in the scene on pages other than the first,
    simply set the parent to the desired page, accessed through the
    global document with `neoscore.document.pages[n]`
    """

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
            pen: The pen to draw outlines with.
            brush: The brush to draw outlines with.
            parent: The parent object or None
        """
        super().__init__(pos, parent)
        self.pen = pen
        self.brush = brush
        self._children: list[GraphicObject] = []

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
            self._pen = Pen.from_existing(DEFAULT_PEN)

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
            self._brush = Brush.from_existing(DEFAULT_BRUSH)
