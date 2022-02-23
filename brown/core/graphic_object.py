from __future__ import annotations

from abc import ABC

from brown import constants
from brown.core import brown
from brown.core.brush import Brush
from brown.core.page import Page
from brown.core.pen import Pen
from brown.utils.point import Point
from brown.utils.units import Mm, Unit


class GraphicObject(ABC):
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
    global document with `brown.document.pages[n]`
    """

    default_pen = Pen(
        constants.DEFAULT_PEN_COLOR,
        constants.DEFAULT_PEN_THICKNESS,
        constants.DEFAULT_PEN_PATTERN,
    )
    _default_brush = Brush(
        constants.DEFAULT_BRUSH_COLOR, constants.DEFAULT_BRUSH_PATTERN
    )

    def __init__(self, pos, length=None, pen=None, brush=None, parent=None):
        """
        Args:
            pos (Point[Unit] or tuple): The position of the object
                relative to its parent
            length (Unit): The width of the object which can be
                subject to breaking across lines when in a`Flowable`.
                If the object is not inside a `Flowable`,
                this has no effect
            pen (Pen): The pen to draw outlines with.
            brush (Brush): The brush to draw outlines with.
            parent (GraphicObject): The parent object or None
        """
        self.pos = pos
        self._length = length if length else Unit(0)
        self.pen = pen
        self.brush = brush
        self._children = []
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
        self._pos = value

    @property
    def x(self):
        """Unit: The x position of the object relative to its parent."""
        return self.pos.x

    @x.setter
    def x(self, value):
        self.pos = Point(value, self.y)

    @property
    def y(self):
        """Unit: The x position of the object relative to its parent."""
        return self.pos.y

    @y.setter
    def y(self, value):
        self.pos = Point(self.x, value)

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
            value = Pen.from_existing(self.default_pen)
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
            value = Brush.from_existing(self._default_brush)
        self._brush = value

    @property
    def parent(self):
        """GraphicObject: The parent object.

        If this is set to None, it defaults to the first page of the document.
        """
        return self._parent

    @parent.setter
    def parent(self, value):
        if hasattr(self, "_parent") and self._parent is not None:
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
    def descendants(self):
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
    def ancestors(self):
        """iter[GraphicObject]: All ancestors of this object.

        Follows the chain of parents until a document page is reached.
        The iterable will *not* include the document `Page`.

        The order begins with `self.parent` and traverses upward in the tree.
        """
        ancestor = self.parent
        while type(ancestor) != Page:
            yield ancestor
            ancestor = ancestor.parent

    @property
    def flowable(self):
        """Flowable or None: The flowable this object belongs in."""
        return self.first_ancestor_of_exact_class("Flowable")

    @property
    def page_index(self):
        """The index of the page this object appears on.

        >>> from brown.core import brown; brown.setup()
        >>> some_object = GraphicObject((Mm(20), Mm(50)),
        ...                             parent=brown.document.pages[5])
        >>> some_object.page_index
        5
        >>> some_object in brown.document.pages[5].descendants
        True

        """
        # The page will be the parent of the final ancestor
        ancestor = None
        for ancestor in self.ancestors:
            pass
        if ancestor is None:
            # self.parent is a page
            return self.parent.page_index
        return ancestor.parent.page_index

    ######## CLASS METHODS ########

    @classmethod
    def map_between_items(cls, source: GraphicObject, dest: GraphicObject) -> Point:
        """Find a GraphicObject's position relative to another

        Args:
            source: The object to map from
            dest: The object to map to

        Returns:
            The canvas position of `dest` relative to `source`
        """
        # Handle easy cases
        if source == dest:
            return Point(Unit(0), Unit(0))
        if source.parent == dest.parent:
            return dest.pos - source.pos
        if dest.parent == source:
            return dest.pos
        if source.parent == dest:
            return -source.pos
        # Otherwise, inefficiently compare the canvas positions of the two objects
        return brown.document.canvas_pos_of(dest) - brown.document.canvas_pos_of(source)

    # TODO can't implement this until document methods are made too
    # @classmethod
    # def map_x_between_items(cls, source: GraphicObject, dest: GraphicObject) -> Unit:
    #     """Specialized version of `map_between_items` which only finds the x delta"""
    #     # Handle easy cases
    #     if source == dest:
    #         return Unit(0)
    #     if source.parent == dest.parent:
    #         return dest.x - source.x
    #     if dest.parent == source:
    #         return dest.x
    #     if source.parent == dest:
    #         return -source.x
    #     # Otherwise, inefficiently compare the canvas positions of the two objects
    #     return brown.document.canvas_pos_of(dest) - brown.document.canvas_pos_of(source)

    ######## PUBLIC METHODS ########

    def descendants_of_class_or_subclass(self, graphic_object_class):
        """Yield all child descendants with a given class or its subclasses.

        Args: graphic_object_class (type): The type to search for.
            This should be a subclass of GraphicObject.

        Yields: GraphicObject
        """
        for descendant in self.descendants:
            if isinstance(descendant, graphic_object_class):
                yield descendant

    def descendants_of_exact_class(self, graphic_object_class):
        """Yield all child descendants with a given class.

        Args: graphic_object_class (type): The type to search for.
            This should be a subclass of GraphicObject.

        Yields: GraphicObject
        """
        for descendant in self.descendants:
            if type(descendant) == graphic_object_class:
                yield descendant

    def first_ancestor_of_class_or_subclass(self, graphic_object_class):
        """Get the closest ancestor with a class or its subclasses.

        If none can be found, returns `None`.

        Args:
            graphic_object_class (type): The type to search for.
                This should be a subclass of GraphicObject.

        Returns: GraphicObject or None
        """
        return next(
            (item for item in self.ancestors if isinstance(item, graphic_object_class)),
            None,
        )

    def first_ancestor_of_exact_class(self, graphic_object_class):
        """Get the closest ancestor with a class.

        If none can be found, returns `None`.

        Args:
            graphic_object_class (type or str): The type to search for.
                This should be a subclass of GraphicObject.
                A str of a class name may also be used.

        Returns: GraphicObject or None
        """
        if isinstance(graphic_object_class, str):
            return next(
                (
                    item
                    for item in self.ancestors
                    if type(item).__name__ == graphic_object_class
                ),
                None,
            )
        return next(
            (item for item in self.ancestors if type(item) == graphic_object_class),
            None,
        )

    def remove(self):
        """Remove this object from the document."""
        if self.parent:
            self.parent.children.remove(self)

    ######## PRIVATE METHODS ########

    def _pre_render_hook(self):
        """Run code once just before document rendering begins.

        This is an experimental feature to support precomputation and
        caching for expensive methods.

        Any data cached in this function must be cleared in a
        corresponding `_post_render_hook`.
        """
        pass

    def _post_render_hook(self):
        """Run code once after document rendering completes.

        Any cached data stored in `_pre_render_hook` must be cleared
        in this function.
        """
        pass

    def _render(self):
        """Render the object and all its children.

        Returns: None
        """
        if self.flowable is not None:
            self._render_in_flowable()
        else:
            self._render_complete(brown.document.canvas_pos_of(self))
        for child in self.children:
            child._render()

    def _register_child(self, child):
        """Add an object to `self.children`.

        Args:
            child (GraphicObject): The object to add

        Returns: None
        """
        self.children.append(child)

    def _unregister_child(self, child):
        """Remove an object from `self.children`.

        Args:
            child (GraphicObject): The object to remove

        Returns: None
        """
        self.children.remove(child)

    def _render_in_flowable(self):
        """Render the object to the scene, dispatching partial rendering calls
        when needed if an object flows across a break in the flowable.

        Returns: None
        """
        # Calculate position within flowable
        pos_in_flowable = self.flowable.pos_in_flowable_of(self)

        remaining_x = self.length + self.flowable.dist_to_line_end(pos_in_flowable.x)
        if remaining_x < Unit(0):
            self._render_complete(
                brown.document.canvas_pos_of(self),
                self.flowable.dist_to_line_start(pos_in_flowable.x),
                pos_in_flowable.x,
            )
            return

        # Render before break
        first_line_i = self.flowable.last_break_index_at(pos_in_flowable.x)
        current_line = self.flowable.layout_controllers[first_line_i]
        render_start_pos = brown.document.canvas_pos_of(self)
        first_line_length = self.flowable.dist_to_line_end(pos_in_flowable.x) * -1
        render_end_pos = Point(
            render_start_pos.x + first_line_length, render_start_pos.y
        )
        self._render_before_break(
            pos_in_flowable.x,
            render_start_pos,
            render_end_pos,
            self.flowable.dist_to_line_start(pos_in_flowable.x),
        )

        # Iterate through remaining length
        for current_line_i in range(
            first_line_i + 1, len(self.flowable.layout_controllers)
        ):
            current_line = self.flowable.layout_controllers[current_line_i]
            if remaining_x > current_line.length:
                # Render spanning continuation
                line_pos = brown.document.canvas_pos_of(current_line)
                render_start_pos = Point(line_pos.x, line_pos.y + pos_in_flowable.y)
                render_end_pos = Point(
                    render_start_pos.x + current_line.length, render_start_pos.y
                )
                self._render_spanning_continuation(
                    self.length - remaining_x, render_start_pos, render_end_pos
                )
                remaining_x -= current_line.length
            else:
                break

        # Render end
        render_start_pos = self.flowable.map_to_canvas(
            Point(current_line.local_x, pos_in_flowable.y)
        )
        render_end_pos = Point(render_start_pos.x + remaining_x, render_start_pos.y)
        self._render_after_break(
            self.length - remaining_x, render_start_pos, render_end_pos
        )

    def _render_complete(self, pos, dist_to_line_start=None, local_start_x=None):
        """Render the entire object.

        This is used to render all objects outside of `Flowable`s,
        as well as those inside flowables when they fit completely in
        one span of the flowable.

        This method should create a GraphicInterface and store it in
        `self.interfaces`.

        Args:
            pos (Point): The rendering position in document space for drawing.
            dist_to_line_start (Unit): If in a `Flowable`,
                the x-axis distance from the active `NewLine`s beginning.
                Otherwise, this is always `None`. Subclasses may use this
                information to perform basic position modifications at
                render time, though in most cases this field can be ignored.
            local_start_x (Unit): If this object is in a flowable, the local
                starting position of this drawing segment.

        Returns: None

        Note: All GraphicObject subclasses should implement this
              for correct rendering.
        """
        raise NotImplementedError

    def _render_before_break(self, local_start_x, start, stop, dist_to_line_start):
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
            dist_to_line_start (Unit): The x-axis distance from the active
                `NewLine`s beginning. Subclasses may use this
                information to perform basic position modifications at
                render time, though in most cases this field can be ignored.

        Returns: None

        Note: All GraphicObject subclasses whose `length` can
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

        Note: All GraphicObject subclasses whose `length` can
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

        Note: All GraphicObject subclasses whose `length` can
              be nonzero must implement this method.
        """
        raise NotImplementedError
