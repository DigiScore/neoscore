"""Objects representing individual elements of :obj:`.Path`\ s.

With the exception of ``CurveTo``, each of these classes is just a bare
``PositionedObject``.
"""


from __future__ import annotations

from neoscore.core.positioned_object import PositionedObject


class PathElement(PositionedObject):
    """Superclass for all path element types"""

    def __repr__(self) -> str:
        return f"{type(self).__name__}(pos={self.pos}, parent={self.parent})"


class MoveTo(PathElement):
    """An element representing the start of a new subpath"""


class LineTo(PathElement):
    """An element representing a straight line from the last path position"""


class ControlPoint(PathElement):
    """An element used as a control point in bezier curves.

    This element is not directly kept in :obj:`.Path.elements`, instead being placed
    inside :obj:`.CurveTo` elements.
    """


class CurveTo(PathElement):
    def __init__(
        self,
        pos: PointDef,
        parent: PositionedObject,
        control_1: ControlPoint,
        control_2: ControlPoint,
    ):
        """
        Args:
            pos: The position of the object relative to its parent
            parent: The parent object.
            control_1: The curve's first control point
            control_2: The curve's second control point
        """
        super().__init__(pos, parent)
        self.control_1 = control_1
        self.control_2 = control_2

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(pos={self.pos}, parent={self.parent},"
            + f" c1={self.control_1}, c2={self.control_2})"
        )
