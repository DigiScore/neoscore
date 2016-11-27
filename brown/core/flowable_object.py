from brown.core.graphic_object import GraphicObject
from brown.utils.point import Point
from brown.utils.units import GraphicUnit
from brown.core.flowable_frame import FlowableFrame


class NoAncestorFlowableFrameError(Exception):
    """Raised when no frame is found in the parentage sequence of a FlowableObject"""
    pass


class FlowableObject(GraphicObject):

    """A GraphicObject in a flowable frame.

    FlowableObjects can have multiple representations calculated at
    render-time. For instance a long line may be cut across line/page breaks
    in the frame.

    To make a concrete FlowableObject class which doesn't break across lines
    (e.g. atomic glyphs), set `self.breakable_width = 0` and override
    `self.render()` instead of the private render helper methods.
    """

    def __init__(self, pos, breakable_width, parent, pen=None, brush=None):
        """
        Args:
            pos (Point[Unit] or tuple): The position of the object
                relative to its parent
            breakable_width (Unit): The drawable breakable_width of this object.
            frame (FlowableFrame): The FlowableFrame this object belongs in.
            pen (Pen): The pen to draw outlines with.
            brush (Brush): The brush to draw outlines with.
            parent (FlowableObject): The parent object or None.
                parents of `FlowableObject`s must all have the same `frame`
        """
        self._interface_list = []
        self._breakable_width = breakable_width
        # TODO: Unify constructor signature argument order across codebase
        super().__init__(pos, pen, brush, parent)

    # TODO: Combine frame and parent more seamlessly.
    #       Earlier implementation of StaffObject parent/staff
    #       is a good model for this.

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self):
        """Point: The position of the object relative to its parent."""
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = Point.with_unit(value, unit=GraphicUnit)
        #if self._interface:
        #    self._interface.pos = self._pos

    @property
    def x(self):
        """Unit: The x position of the object relative to its parent."""
        return self.pos.x

    @x.setter
    def x(self, value):
        self.pos.x = value
        #if self._interface:
        #    self._interface.x = value

    @property
    def y(self):
        """Unit: The x position of the object relative to its parent."""
        return self.pos.y

    @y.setter
    def y(self, value):
        self.pos.y = value
        #if self._interface:
        #    self._interface.y = value

    @property
    def pen(self):
        """Pen: The pen to draw outlines with"""
        return self._pen

    @pen.setter
    def pen(self, value):
        self._pen = value
        #if self._pen and self._interface:
        #    self._interface.pen = self._pen._interface

    @property
    def brush(self):
        """Brush: The brush to draw outlines with"""
        return self._brush

    @brush.setter
    def brush(self, value):
        self._brush = value
        #if self._brush and self._interface:
            #self._interface.brush = self._brush._interface

    @property
    def parent(self):
        """GraphicObject: The parent object"""
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        #if self._interface:
        #    if value is not None:
        #        self._interface.parent = value._interface
        #    else:
        #        self._interface.parent = None

    @property
    def frame(self):
        """FlowableFrame: The frame this object belongs in.

        This property is read-only
        """
        try:
            ancestor = self.parent
            while not isinstance(ancestor, FlowableFrame):
                ancestor = ancestor.parent
            return ancestor
        except AttributeError:
            raise NoAncestorFlowableFrameError

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
    def document_pos(self):
        """Point: The position of the object in document space."""
        return self.frame._local_space_to_doc_space(self.pos)

    ######## PRIVATE PROPERTIES ########

    @property
    def _interfaces(self):
        """list[GraphicObjectInterface]: The interfaces for the object.

        Unlike a common GraphicObject which has exactly one
        GraphicObjectInterface, FlowableObjects can have multiple discreet
        graphical representations (created by the various partial
        rendering methods.)

        This property is read-only.
        """
        return self._interface_list

    ######## PUBLIC METHODS ########

    def render(self):
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

    ######## PRIVATE METHODS ########

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
