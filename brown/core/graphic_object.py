from abc import ABC

from brown import config
from brown.core import brown
from brown.core.brush import Brush
from brown.core.pen import Pen
from brown.utils.point import Point
from brown.utils.units import Unit, Mm


class GraphicObject(ABC):
    """An abstract graphic object.

    All classes in `core` which have the ability to be displayed
    should be subclasses of this.

    A single GraphicObject can have multiple graphical representations,
    calculated at render-time. If the object's ancestor is a FlowableFrame,
    it will be rendered as a flowable object, capable of being wrapped around
    lines.

    The position of this object is relative to that of its parent.
    Each GraphicObject has another GraphicObject for a parent, except
    `Page` objects, whose parent is always the global `Document`.

    For convenience, the parent may be initialized to None to indicate
    the first page of the document.

    To place objects directly in the scene on pages other than the first,
    simply set the parent to the desired page, accessed through the
    global document with `brown.document.pages[n]`
    """

    default_pen = Pen(config.DEFAULT_PEN_COLOR,
                      config.DEFAULT_PEN_THICKNESS,
                      config.DEFAULT_PEN_PATTERN)
    _default_brush = Brush(config.DEFAULT_BRUSH_COLOR,
                           config.DEFAULT_BRUSH_PATTERN)

    def __init__(self, pos, length=None,
                 pen=None, brush=None, parent=None):
        """
        Args:
            pos (Point[Unit] or tuple): The position of the object
                relative to its parent
            length (Unit): The width of the object which can be
                subject to breaking across lines when in a`FlowableFrame`.
                If the object is not inside a `FlowableFrame`,
                this has no effect
            pen (Pen): The pen to draw outlines with.
            brush (Brush): The brush to draw outlines with.
            parent (GraphicObject): The parent object or None
        """
        self.pos = pos
        self._length = length if length else Unit(0)
        self.pen = pen
        self.brush = brush
        self._children = set()
        self.parent = parent
        self._interfaces = set()

    ######## PUBLIC PROPERTIES ########

    @property
    def interfaces(self):
        """set(GraphicObjectInterface): The interfaces for this object

        Interface objects are created upon calling `GraphicObject.render()`

        Typically each GraphicObject will have one interface for each
        flowable line it appears in. Objects which fit completely
        in one visual line will typically have exactly one interface.

        If this is an empty set, the object has not been rendered yet
        with the `render()` method.
        """
        return self._interfaces

    @property
    def pos(self):
        """Point: The position of the object relative to its parent."""
        return self._pos

    @pos.setter
    def pos(self, value):
        if not isinstance(value, Point):
            value = Point(*value)
        else:
            value = Point.from_existing(value)
        self._pos = value

    @property
    def x(self):
        """Unit: The x position of the object relative to its parent."""
        return self.pos.x

    @x.setter
    def x(self, value):
        self.pos.x = value

    @property
    def y(self):
        """Unit: The x position of the object relative to its parent."""
        return self.pos.y

    @y.setter
    def y(self, value):
        self.pos.y = value

    @property
    def length(self):
        """Unit: The breakable length of the object.

        This is used to determine how and where rendering cuts should be made.
        """
        return self._length

    @property
    def pen(self):
        """Pen: The pen to draw outlines with"""
        return self._pen

    @pen.setter
    def pen(self, value):
        if value:
            if isinstance(value, str):
                value = Pen(value)
            elif isinstance(value, Pen):
                pass
            else:
                raise TypeError
        else:
            value = Pen.from_existing(type(self).default_pen)
        self._pen = value

    @property
    def brush(self):
        """Brush: The brush to draw outlines with

        As a convenience, this may be set with a hex color string
        for a solid color brush of that color. For brushes using
        alpha channels and non-solid-color fill patterns, a fully
        initialized brush must be passed to this.
        """
        return self._brush

    @brush.setter
    def brush(self, value):
        if value:
            if isinstance(value, str):
                value = Brush(value)
            elif isinstance(value, Brush):
                pass
            else:
                raise TypeError
        else:
            value = Brush.from_existing(type(self)._default_brush)
        self._brush = value

    @property
    def parent(self):
        """GraphicObject: The parent object.

        If this is set to None, it defaults to the first page of the document.
        """
        return self._parent

    @parent.setter
    def parent(self, value):
        if hasattr(self, '_parent') and self._parent is not None:
            self._parent._unregister_child(self)
        if value is None:
            value = brown.document.pages[0]
        self._parent = value
        self._parent._register_child(self)

    @property
    def children(self):
        """set(GraphicObject): All objects who have self as their parent."""
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    @property
    def all_descendants(self):
        """iter[GraphicObject]: All of the objects in the children subtree.

        This recursively searches all of the object's children
        (and their children, etc.) and provides an iterator over them.

        The current implementation performs a simple recursive DFS over
        the tree, and has the potential to be rather slow.
        """
        for child in self.children:
            for subchild in child.children:
                yield subchild
            yield child

    @property
    def frame(self):
        """FlowableFrame or None: The frame this object belongs in."""
        try:
            ancestor = self.parent
            while type(ancestor).__name__ != 'FlowableFrame':
                ancestor = ancestor.parent
            return ancestor
        except AttributeError:
            return None

    @property
    def page_index(self):
        """The index of the page this object appears on.

            >>> from brown.core import brown; brown.setup()
            >>> some_object = GraphicObject((Mm(20), Mm(50)),
            ...                             parent=brown.document.pages[5])
            >>> some_object.page_index
            5
            >>> some_object in brown.document.pages[5].all_descendants
            True

        """
        # Traverse the parent chain until a page is found and returns its index
        ancestor = self.parent
        while type(ancestor).__name__ != 'Page':
            ancestor = ancestor.parent
        return ancestor.page_index

    @property
    def is_in_flowable(self):
        """bool: Whether or not this object is in a FlowableFrame"""
        return (self.frame is not None)

    ######## CLASS METHODS ########

    @classmethod
    def map_between_items(cls, source, destination):
        """Find a GraphicObject's position relative to another GraphicObject

        Args:
            source (GraphicObject): The object to map from
            destination (GraphicObject): The object to map to

        Returns:
            Point: The canvas position of `destination` relative to `source`
        """
        # inefficient for now - find position relative to doc root of both
        # and find delta between the two.
        return (brown.document.canvas_pos_of(destination) -
                brown.document.canvas_pos_of(source))

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the object and all its children.

        Returns: None
        """
        if self.is_in_flowable:
            self._render_flowable()
        else:
            self._render_complete(brown.document.canvas_pos_of(self))
        for child in self.children:
            child.render()

    def all_descendants_with_class_or_subclass(self, graphic_object_class):
        """Yield all child descendants with a given class or its subclasses.

        Args: graphic_object_class (type): The type to search for.
            This should be a subclass of GraphicObject.

        Yields: GraphicObject
        """
        for descendant in self.all_descendants:
            if isinstance(descendant, graphic_object_class):
                yield descendant

    def all_descendants_with_exact_class(self, graphic_object_class):
        """Yield all child descendants with a given class.

        Args: graphic_object_class (type): The type to search for.
            This should be a subclass of GraphicObject.

        Yields: GraphicObject
        """
        for descendant in self.all_descendants:
            if type(descendant) == graphic_object_class:
                yield descendant

    ######## PRIVATE METHODS ########

    def _register_child(self, child):
        """Add an object to `self.children`.

        Args:
            child (GraphicObject): The object to add

        Returns: None
        """
        self.children.add(child)

    def _unregister_child(self, child):
        """Remove an object from `self.children`.

        Args:
            child (GraphicObject): The object to remove

        Returns: None
        """
        self.children.remove(child)

    def _render_flowable(self):
        """Render the object to the scene, dispatching partial rendering calls
        when needed if an object flows across a break in the frame.

        Returns: None
        """
        # Calculate position within flowable
        pos_in_flowable = self.frame.pos_in_frame_of(self)

        remaining_x = (self.length +
                       self.frame._dist_to_line_end(pos_in_flowable.x))
        if remaining_x < Unit(0):
            self._render_complete(brown.document.canvas_pos_of(self))
            return

        # Render before break
        first_line_i = self.frame._last_break_index_at(pos_in_flowable.x)
        current_line = self.frame.layout_controllers[first_line_i]
        render_start_pos = brown.document.canvas_pos_of(self)
        first_line_length = self.frame._dist_to_line_end(pos_in_flowable.x) * -1
        render_end_pos = (render_start_pos + Point(first_line_length, 0))
        self._render_before_break(Unit(0), render_start_pos, render_end_pos)

        # Iterate through remaining length
        for current_line_i in range(first_line_i + 1,
                                    len(self.frame.layout_controllers)):
            current_line = self.frame.layout_controllers[current_line_i]
            if remaining_x > current_line.length:
                # Render spanning continuation
                line_pos = brown.document.canvas_pos_of(current_line)
                render_start_pos = Point(line_pos.x,
                                         line_pos.y + pos_in_flowable.y)
                render_end_pos = render_start_pos + Point(current_line.length, 0)
                self._render_spanning_continuation(
                    self.length - remaining_x,
                    render_start_pos,
                    render_end_pos)
                remaining_x -= current_line.length
            else:
                break

        # Render end
        render_start_pos = self.frame._map_to_canvas(
            Point(current_line.local_x, pos_in_flowable.y))
        render_end_pos = render_start_pos + Point(remaining_x, 0)
        self._render_after_break(self.length - remaining_x,
                                 render_start_pos,
                                 render_end_pos)

    def _render_complete(self, pos):
        """Render the entire object.

        For use in flowable containers when rendering a FlowableObject
        which happens to completely fit within a span of the FlowableFrame.
        This function should render the entire object at `self.pos`

        This method should create a GraphicInterface and store it in
        `self.interfaces`.

        Args:
            pos (Point): The rendering position in document space for drawing.

        Returns: None

        Note: All GraphicObject subclasses should implement this
              for correct rendering.
        """
        raise NotImplementedError

    def _render_before_break(self, local_start_x, start, stop):
        """Render the beginning of the object up to a stopping point.

        For use in flowable containers when rendering an object that
        crosses a line or page break. This function should render the
        beginning portion of the object up to the break.

        This method should create a GraphicInterface and store it in
        `self.interfaces`.

        Args:
            local_start_x (Unit): The local starting position of this
                drawing segment.
            start (Point): The starting point in document space for drawing.
            stop (Point): The stopping point in document space for drawing.

        Returns: None

        Note: Any GraphicObject subclasses whose length can
              be nonzero must implement this method.
        """
        raise NotImplementedError

    def _render_after_break(self, local_start_x, start, stop):
        """Render the continuation of an object after a break.

        For use in flowable containers when rendering an object that
        crosses a line or page break. This function should render the
        ending portion of an object after a break.

        This method should create a GraphicInterface and store it in
        `self.interfaces`.

        Args:
            local_start_x (Unit): The local starting position of this
                drawing segment.
            start (Point): The starting point in document space for drawing.
            stop (Point): The stopping point in document space for drawing.

        Returns: None

        Note: Any GraphicObject subclasses whose length can
              be nonzero must implement this method.
        """
        raise NotImplementedError

    def _render_spanning_continuation(self, local_start_x, start, stop):
        """
        Render the continuation of an object after a break and before another.

        For use in flowable containers when rendering an object that crosses
        two breaks. This function should render the portion of the object
        surrounded by breaks on either side.

        This method should create a GraphicInterface and store it in
        `self.interfaces`.

        Args:
            local_start_x (Unit): The local starting position of this
                drawing segment.
            start (Point): The starting point in document space for drawing.
            stop (Point): The stopping point in document space for drawing.

        Returns: None

        Note: Any GraphicObject subclasses whose length can
              be nonzero must implement this method.
        """
        raise NotImplementedError
