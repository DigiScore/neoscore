from PyQt5 import QtGui

from brown.core import brown
from brown.core.path_element_type import PathElementType
from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.interface.path_element_interface import PathElementInterface
from brown.interface.qt.q_clipping_path import QClippingPath
from brown.utils.point import Point
from brown.utils.units import GraphicUnit

"""
Qt paths have a few quirks which are good to know about if you're
working with them at a lower level.

At creation time, paths have `elementCount() == 0`,
but after a line is created, `elementCount() == 2`. The first element
is a `moveTo` to the origin; second is the `lineTo` you asked for.
`brown` paths maintain this behavior.

TODO: This is out of date and may not be true.

If a `lineTo(0, 0)`, a `moveTo(0, 0)` is performed instead:

    >>> from brown.core import brown; brown.setup()
    >>> line_to_origin = PathInterface((5, 6))
    >>> line_to_origin.line_to((0, 0))
    >>> assert(line_to_origin._qt_path == line_to_origin.qt_object.path())
    >>> assert(line_to_origin._qt_path.elementCount() == 1)
    >>> assert(line_to_origin._qt_path.elementAt(0).isMoveTo() == True)
    >>> line_to_elsewhere = PathInterface((5, 6))
    >>> line_to_elsewhere.line_to((1, 0))
    >>> assert(line_to_elsewhere._qt_path == line_to_elsewhere.qt_object.path())
    >>> assert(line_to_elsewhere._qt_path.elementCount() == 2)
    >>> assert(line_to_elsewhere._qt_path.elementAt(0).isMoveTo() == True)
    >>> assert(line_to_elsewhere._qt_path.elementAt(1).isLineTo() == True)

`QPainterPath::ElementType` is ambiguous in differentiating between
curve control points and curve end points. They are stored sequentially
in the path element list; the first element in the sequence is a
`CurveToElement` (enum 2), all following elements in the curve are
`CurveToDataElement` (enum 3). Despite this, all elements until the last
in the sequence are control points; the final element is the curve end point.

For instance, if a cubic line is drawn with two control points -
`cubic_to((0, 5), (10, 5), (10, 0))` - they are stored in the Qt
element list as `[CurveToElement, CurveToDataElement, CurveToDataElement]`,
which the brown API translates to: `[control_point, control_point, curve_to]`
"""


class PathInterface(GraphicObjectInterface):
    """Interface for a generic graphic path object."""
    def __init__(self, brown_object, pos, pen, brush,
                 clip_start_x=None, clip_width=None):
        """
        Args:
            brown_object (Path): The path this interface belongs to
            pos (Point[GraphicUnit] or tuple): The position of the path root
                relative to the document.
            pen (PenInterface): The pen to draw outlines with.
            brush (BrushInterface): The brush to draw outlines with.
            clip_start_x (Unit or None): The local starting position for the
                path clipping region. Use `None` to render from the start.
            clip_width (Unit or None): The width of the path clipping region.
                Use `None` to render to the end
        """
        super().__init__(brown_object)
        self.qt_path = QtGui.QPainterPath()
        self.qt_object = QClippingPath(self.qt_path,
                                        clip_start_x, clip_width)
        self.pos = pos
        self.pen = pen
        self.brush = brush
        self.clip_start_x = clip_start_x
        self.clip_width = clip_width

    ######## PUBLIC PROPERTIES ########

    @property
    def current_draw_pos(self):
        """Point[GraphicUnit]: The current relative drawing position.

        This is the location from which operations like line_to() will draw,
        relative to the position of the Path (`self.x` and `self.y`).

        This property is read-only. To move the current position, use
        the move_to() method, implicitly closing the current sub-path and
        beginning a new one.
        """
        if self.element_count:
            return self.element_at(-1).pos
        else:
            return Point(0, 0)

    @property
    def element_count(self):
        """int: The number of elements in the path."""
        return self.qt_path.elementCount()

    ######## Public Methods ########

    # TODO: Update signatures to reflect new Path API

    def update_geometry(self):
        self.qt_object.update_geometry()

    def line_to(self, pos):
        """Draw a path from the current position to a new point.

        Connect a path from the current position to a new position specified
        by `pos`, and move `self.current_draw_pos` to the new point.

        Args:
            pos (Point or tuple): The target position

        Returns: None
        """
        target = Point(pos.x, pos.y).to_unit(GraphicUnit)
        self.qt_path.lineTo(target.x.value, target.y.value)
        self.update_qt_path()

    def cubic_to(self,
                 control_1,
                 control_2,
                 end):
        """Draw a cubic spline from the current position to a new point.

        Moves `self.current_draw_pos` to the new end point.

        Args:
            control_1 (Point): The local position of the 1st control point
            control_2 (Point): The local position of the 2nd control point
            end (Point): The local position of the end point

        Returns: None
        """
        control_1_point = Point(control_1.x, control_1.y).to_unit(GraphicUnit)
        control_2_point = Point(control_2.x, control_2.y).to_unit(GraphicUnit)
        end_point = Point(end.x, end.y).to_unit(GraphicUnit)
        self.qt_path.cubicTo(
            control_1_point.x.value,
            control_1_point.y.value,
            control_2_point.x.value,
            control_2_point.y.value,
            end_point.x.value,
            end_point.y.value)
        self.update_qt_path()

    def move_to(self, pos):
        """Close the current sub-path and start a new one.

        Args:
            pos (Point or tuple): The target position

        Returns: None
        """
        target = Point(pos.x, pos.y).to_unit(GraphicUnit)
        self.qt_path.moveTo(target.x.value, target.y.value)
        self.update_qt_path()

    def close_subpath(self):
        """Close the current sub-path and start a new one at (0, 0).

        This is equivalent to `move_to(0, 0)`

        Returns: None
        """
        self.qt_path.closeSubpath()
        self.update_qt_path()

    def element_at(self, index):
        """Find the element at a given index and return it.

        Args:
            index (int): The element index. Use -1 for the last index.

        Returns: PathElementInterface

        # TODO: Implement a list-like iterable wrapper around path elements?
        """
        if index < 0:
            # Allow pythonic negative indexing
            qt_index = self.element_count + index
        else:
            qt_index = index
        qt_element = self.qt_path.elementAt(qt_index)
        # Determine the element type
        if qt_element.type == 0:
            element_type = PathElementType.move_to
        elif qt_element.type == 1:
            element_type = PathElementType.line_to
        elif qt_element.type == 2:
            # First element in curve sequence is always a control point
            element_type = PathElementType.control_point
        else:
            # Otherwise to distinguish control point from curve,
            # look right and find if this is the last element before
            # something other than 3. See module note for more detail.
            if (qt_index == self.element_count or
                    self.qt_path.elementAt(qt_index + 1).type != 3):
                element_type = PathElementType.curve_to
            else:
                element_type = PathElementType.control_point
        return PathElementInterface(qt_element, self, qt_index, element_type)

    def set_element_position_at(self, index, pos):
        """Set the element at an index to a given position.

        Args:
            index (int): The element index to modify
            pos (Point[Unit]): The new position for the element.

        Returns: None
        """
        if index > self.qt_path.elementCount():
            raise IndexError(
                'Element index {} out of bounds (max is {})'.format(
                    index, self.qt_path.elementCount()))
        self.qt_path.setElementPositionAt(index,
                                           GraphicUnit(pos.x).value,
                                           GraphicUnit(pos.y).value)
        self.update_qt_path()

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        brown._app_interface.scene.addItem(self.qt_object)

    def update_qt_path(self):
        """Synchronize the contents of self.qt_path to self.qt_object

        Returns: None
        """
        self.qt_object.setPath(self.qt_path)
