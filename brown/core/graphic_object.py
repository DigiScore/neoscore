from abc import ABC

from brown.config import config
from brown.core.flowable_frame import FlowableFrame
from brown.utils.units import Unit, GraphicUnit
from brown.utils.point import Point


class GraphicObject(ABC):
    """An abstract graphic object.

    All classes in `core` which have the ability to be displayed
    should be subclasses of this.

    A single GraphicObject can have multiple graphical representations,
    calculated at render-time. If the object's ancestor is a FlowableFrame,
    it will be rendered as a flowable object, capable of being wrapped around
    lines.

    TODO: Flesh out the expected way subclasses should be made.
          Right now it's pretty patchy -- _interface isn't even documented
          at all...
    """
    def __init__(self, pos, breakable_width=0,
                 pen=None, brush=None, parent=None):
        """
        Args:
            pos (Point[Unit] or tuple): The position of the object
                relative to its parent
            breakable_width (Unit): The width of the object which can be
                subject to breaking across line breaks when in a FlowableFrame.
                If the object is not inside a FlowableFrame, this has no effect
            pen (Pen): The pen to draw outlines with.
            brush (Brush): The brush to draw outlines with.
            parent (GraphicObject): The parent object or None
        """
        self.pos = pos
        self._breakable_width = breakable_width
        self.pen = pen
        self.brush = brush
        self.parent = parent

    ######## PUBLIC PROPERTIES ########

    # @property
    # def _interface(self):
    #     """GraphicObjectInterface: The interface for the object.

    #     This property is read-only.
    #     """
    #     return self.__interface

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self):
        """Point: The position of the object relative to its parent."""
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = Point.with_unit(value, unit=GraphicUnit)
        if self._interface:
            self._interface.pos = self._pos

    @property
    def x(self):
        """Unit: The x position of the object relative to its parent."""
        return self.pos.x

    @x.setter
    def x(self, value):
        self.pos.x = value
        if self._interface:
            self._interface.x = value

    @property
    def y(self):
        """Unit: The x position of the object relative to its parent."""
        return self.pos.y

    @y.setter
    def y(self, value):
        self.pos.y = value
        if self._interface:
            self._interface.y = value

    @property
    def breakable_width(self):
        """Unit: The breakable_width of the object.

        This is used to determine how and where rendering cuts should be made.
        """
        return self._breakable_width

    @breakable_width.setter
    def breakable_width(self, value):
        # TODO: Maybe implement me?
        raise NotImplementedError

    @property
    def pen(self):
        """Pen: The pen to draw outlines with"""
        return self._pen

    @pen.setter
    def pen(self, value):
        self._pen = value
        if self._pen and self._interface:
            self._interface.pen = self._pen._interface

    @property
    def brush(self):
        """Brush: The brush to draw outlines with"""
        return self._brush

    @brush.setter
    def brush(self, value):
        self._brush = value
        if self._brush and self._interface:
            self._interface.brush = self._brush._interface

    @property
    def parent(self):
        """GraphicObject: The parent object"""
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        if self._interface and (not self.is_in_flowable):
            if value is not None:
                self._interface.parent = value._interface
            else:
                self._interface.parent = None

    @property
    def frame(self):
        """FlowableFrame or None: The frame this object belongs in.

        This property is read-only
        """
        try:
            ancestor = self.parent
            while not isinstance(ancestor, FlowableFrame):
                ancestor = ancestor.parent
            return ancestor
        except AttributeError:
            return None

    @property
    def is_in_flowable(self):
        """bool: Whether or not this object is in a FlowableFrame"""
        return (self.frame is not None)

    @property
    def document_pos(self):
        """Point: The position of the object in document space."""
        if self.is_in_flowable:
            return self.frame._local_space_to_doc_space(self.pos)
        else:
            raise NotImplementedError  # TODO

    ######## PUBLIC METHODS ########

    def pos_relative_to_item(self, other):
        """Find this object's position relative to another GraphicObject

        Args:
            other (GraphicObject): The object to map from

        Returns: Point
        """
        if self.parent == other:
            return self.pos
        return self._interface.pos_relative_to_item(other._interface)

    def render(self):
        """Render the object to the scene.

        Returns: None
        """
        if self.is_in_flowable:
            self._render_flowable()
        else:
            self._render_complete()

    ######## PRIVATE METHODS ########

    def _render_flowable(self):
        """Render the line to the scene, dispatching partial rendering calls
        when needed if an object flows across a break in the frame.

        Returns: None
        """
        remaining_x = self.breakable_width
        print(remaining_x)
        remaining_x += self.frame._x_pos_rel_to_line_end(self.x)
        if remaining_x < 0:
            self._render_complete()
            return
        first_line_i = self.frame._last_break_index_at(self.x)
        # Render before break
        current_line = self.frame.auto_layout_controllers[first_line_i]
        render_start_pos = self.frame._local_space_to_doc_space(self.pos)
        render_end_pos = render_start_pos + Point(-1 * self.frame._x_pos_rel_to_line_end(self.x), 0)
        self._render_before_break(render_start_pos, render_end_pos)
        # Iterate through remaining breakable_width
        for current_line_i in range(first_line_i + 1, len(self.frame.auto_layout_controllers)):
            current_line = self.frame.auto_layout_controllers[current_line_i]
            if remaining_x > current_line.length:
                remaining_x -= current_line.length
                # Render spanning continuation
                render_start_pos = self.frame._local_space_to_doc_space(
                    Point(current_line.x, self.y))
                render_end_pos = render_start_pos + Point(current_line.length, 0)
                self._render_spanning_continuation(render_start_pos,
                                                   render_end_pos)
            else:
                break
        # Render end
        render_start_pos = self.frame._local_space_to_doc_space(
                    Point(current_line.x, self.y))
        render_end_pos = render_start_pos + Point(remaining_x, 0)
        self._render_after_break(render_start_pos,
                                 render_end_pos)
        # Call render() on interface
        # TODO: May change the way this is handled to letting helper functions
        #       do the interface render()
        self._interface.render()

    def _render_complete(self):
        """Render the entire object.

        For use in flowable containers when rendering a FlowableObject
        which happens to completely fit within a span of the FlowableFrame.
        This function should render the entire object at `self.pos`

        Returns: None

        Note: FlowableObject subclasses should implement this
              for correct rendering.
        """
        raise NotImplementedError

    def _render_before_break(self, start, stop):
        """Render the beginning of the object up to a stopping point.

        For use in flowable containers when rendering an object that
        crosses a line or page break. This function should render the
        beginning portion of the object up to the break.

        Args:
            start (Point): The starting point in document space for drawing.
            stop (Point): The stopping point in document space for drawing.

        Returns: None

        Note: FlowableObject subclasses should implement this
              for correct rendering.
        """
        raise NotImplementedError

    def _render_after_break(self, start, stop):
        """Render the continuation of an object after a break.

        For use in flowable containers when rendering an object that
        crosses a line or page break. This function should render the
        ending portion of an object after a break.

        Args:
            start (Point): The starting point in document space for drawing.
            stop (Point): The stopping point in document space for drawing.

        Returns: None

        Note: FlowableObject subclasses should implement this
              for correct rendering.
        """
        raise NotImplementedError

    def _render_spanning_continuation(self, start, stop):
        """
        Render the continuation of an object after a break and before another.

        For use in flowable containers when rendering an object that
        crosses two breaks. This function should render the
        portion of the object surrounded by breaks on either side.

        Args:
            start (Point): The starting point in document space for drawing.
            stop (Point): The stopping point in document space for drawing.

        Returns: None

        Note: FlowableObject subclasses should implement this
              for correct rendering.
        """
        raise NotImplementedError
