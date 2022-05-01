from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any, Optional, Type, cast

from neoscore.core import neoscore
from neoscore.core.mapping import (
    canvas_pos_of,
    descendant_pos,
    first_ancestor_with_attr,
)
from neoscore.core.point import Point, PointDef
from neoscore.core.units import ZERO, Unit
from neoscore.interface.positioned_object_interface import PositionedObjectInterface

if TYPE_CHECKING:
    # Used in type annotations, imported here to avoid cyclic imports
    from neoscore.core.flowable import Flowable


class PositionedObject:
    """An object positioned in the scene

    This is the base class of all objects in the neoscore scene tree.

    A single PositionedObject can have multiple graphical representations,
    calculated at render-time. If the object's ancestor is a Flowable,
    it will be rendered as a flowable object, capable of being wrapped around
    lines.

    The position of this object is relative to that of its parent.
    Each PositionedObject has another PositionedObject for a parent, except
    ``Page`` objects, whose parent is always the global ``Document``.

    For convenience, the parent may be initialized to None to indicate
    the first page of the document.

    To place objects directly in the scene on pages other than the first,
    simply set the parent to the desired page, accessed through the
    global document with ``neoscore.document.pages[n]``
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
    ):
        """
        Args:
            pos: The position of the object relative to its parent
            parent: The parent object or None
        """
        self.pos = pos
        self._children: list[PositionedObject] = []
        self._parent = PositionedObject._resolve_parent(parent)
        self._set_parent_and_register_self(parent)
        self._interfaces = []

    @property
    def pos(self) -> Point:
        """Point: The position of the object relative to its parent."""
        return self._pos

    @pos.setter
    def pos(self, value: PointDef):
        self._pos = Point.from_def(value)

    @property
    def x(self) -> Unit:
        """The x position of the object relative to its parent."""
        return self.pos.x

    @x.setter
    def x(self, value: Unit):
        self.pos = Point(value, self.y)

    @property
    def y(self) -> Unit:
        """The x position of the object relative to its parent."""
        return self.pos.y

    @y.setter
    def y(self, value: Unit):
        self.pos = Point(self.x, value)

    @property
    def breakable_length(self) -> Unit:
        """The breakable length of the object.

        This is used to determine how and where rendering cuts should
        be made. A length of zero indicates that no rendering cuts
        will be made.

        This is derived from other properties and cannot be set directly.
        """
        return ZERO

    @property
    def parent(self) -> PositionedObject:
        """The parent object.

        If this is set to None, it defaults to the first page of the document.
        """
        return self._parent

    @parent.setter
    def parent(self, value: Optional[PositionedObject]):
        self._parent._unregister_child(self)
        self._set_parent_and_register_self(value)

    @property
    def children(self) -> list[PositionedObject]:
        """All objects who have self as their parent."""
        return self._children

    @children.setter
    def children(self, value: list[PositionedObject]):
        self._children = value

    @property
    def descendants(self) -> Iterator[PositionedObject]:
        """All of the objects in the children subtree.

        This recursively searches all of the object's children
        (and their children, etc.) and provides an iterator over them.

        The current implementation performs a simple recursive DFS over
        the tree, and has the potential to be rather slow.
        """
        for child in self.children:
            for subchild in child.descendants:
                yield subchild
            yield child

    @property
    def flowable(self) -> Optional[Flowable]:
        """The flowable this object belongs in."""
        return cast(
            Any, first_ancestor_with_attr(self, "_neoscore_flowable_type_marker")
        )

    @property
    def interfaces(self) -> list[PositionedObjectInterface]:
        """The graphical backend binding interfaces for this object

        Interface objects are created upon calling ``PositionedObject.render()``

        Typically each PositionedObject will have one interface for each
        flowable line it appears in. Objects which fit completely
        in one visual line will typically have exactly one interface.

        If this is an empty set, the object has not been rendered yet
        with the ``render()`` method.
        """
        return self._interfaces

    def descendants_of_class_or_subclass(
        self, graphic_object_class: Type[PositionedObject]
    ) -> Iterator[PositionedObject]:
        """Yield all child descendants with a given class or its subclasses."""
        for descendant in self.descendants:
            if isinstance(descendant, graphic_object_class):
                yield descendant

    def descendants_of_exact_class(
        self, graphic_object_class: Type[PositionedObject]
    ) -> Iterator[PositionedObject]:
        """Yield all child descendants of a given class, excluding sublcasses"""
        for descendant in self.descendants:
            if type(descendant) == graphic_object_class:
                yield descendant

    def descendants_with_attribute(self, attribute: str) -> Iterator[PositionedObject]:
        """Yield all child descendants which has a given attribute.

        This is useful for searching descendants for duck-typing matches.
        """
        for descendant in self.descendants:
            if hasattr(descendant, attribute):
                yield descendant

    def remove(self):
        """Remove this object from the document."""
        if self.parent:
            self.parent.children.remove(self)

    ######## PRIVATE METHODS ########

    def pre_render_hook(self):
        """Run code once just before document rendering begins.

        This is an experimental feature to support precomputation and
        caching for expensive methods.

        Any data cached in this function must be cleared in a
        corresponding ``post_render_hook``.
        """

    def post_render_hook(self):
        """Run code once after document rendering completes.

        Any cached data stored in ``pre_render_hook`` must be cleared
        in this function.
        """

    def render(self):
        """Render the object and all its children."""
        if self.breakable_length != ZERO and self.flowable is not None:
            self.render_in_flowable()
        else:
            self.render_complete(canvas_pos_of(self))
        for child in self.children:
            child.render()

    def render_in_flowable(self):
        """Render the object to the scene, dispatching partial rendering calls
        when needed if an object flows across a break in the flowable.
        """
        # Calculate position within flowable
        pos_in_flowable = descendant_pos(self, self.flowable)
        dist_to_first_line_end = self.flowable.dist_to_line_end(pos_in_flowable.x)
        remaining_x = self.breakable_length - dist_to_first_line_end
        if remaining_x <= ZERO:
            self.render_complete(
                canvas_pos_of(self),
                self.flowable.dist_to_line_start(pos_in_flowable.x),
                pos_in_flowable.x,
            )
            return

        # Render before break
        first_line_i = self.flowable.last_break_index_at(pos_in_flowable.x)
        current_line = self.flowable.layout_controllers[first_line_i]
        render_start_pos = canvas_pos_of(self)
        first_line_length = dist_to_first_line_end
        render_end_pos = Point(
            render_start_pos.x + first_line_length, render_start_pos.y
        )
        self.render_before_break(
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
                line_pos = canvas_pos_of(current_line)
                render_start_pos = Point(line_pos.x, line_pos.y + pos_in_flowable.y)
                render_end_pos = Point(
                    render_start_pos.x + current_line.length,
                    render_start_pos.y,
                )
                self.render_spanning_continuation(
                    self.breakable_length - remaining_x,
                    render_start_pos,
                    render_end_pos,
                )
                remaining_x -= current_line.length
            else:
                break

        # Render end
        render_start_pos = self.flowable.map_to_canvas(
            Point(current_line.flowable_x, pos_in_flowable.y)
        )
        render_end_pos = Point(render_start_pos.x + remaining_x, render_start_pos.y)
        self.render_after_break(self.breakable_length - remaining_x, render_start_pos)

    def render_complete(
        self,
        pos: Point,
        dist_to_line_start: Optional[Unit] = None,
        local_start_x: Optional[Unit] = None,
    ):
        """Render the entire object.

        This is used to render all objects outside of flowables, as well as those inside
        flowables when they fit completely in one line of the flowable.

        This method should create a GraphicInterface and store it in
        ``self.interfaces``.

        Note: By default this is a no-op. Subclasses with with
        rendered appearances should override this.

        Args:
            pos: The rendering position in document space for drawing.
            dist_to_line_start: If in a ``Flowable``, the x-axis distance from the
                active ``NewLine`` beginning. Otherwise, this is always ``None``.
                Subclasses may use this information to perform basic position
                modifications at render time, though in most cases this field
                can be ignored.
            local_start_x: If this object is in a flowable, the local
                starting position of this drawing segment.

        """

    def render_before_break(
        self, local_start_x: Unit, start: Point, stop: Point, dist_to_line_start: Unit
    ):
        """Render the beginning of the object up to a stopping point.

        For use in flowable containers when rendering an object that
        crosses a line or page break. This function should render the
        beginning portion of the object up to the break.

        This method should create a GraphicInterface and store it in
        ``self.interfaces``.

        Args:
            local_start_x: The local starting position of this
                drawing segment.
            start: The starting point in document space for drawing.
            stop: The stopping point in document space for drawing.
            dist_to_line_start: The x-axis distance from the active
                ``NewLine`` beginning. Subclasses may use this
                information to perform basic position modifications at
                render time, though in most cases this field can be ignored.

        Note: By default this is a no-op. Subclasses with with
            rendered appearances should override this.
        """

    def render_after_break(self, local_start_x: Unit, start: Point):
        """Render the continuation of an object after a break.

        For use in flowable containers when rendering an object that
        crosses a line or page break. This function should render the
        ending portion of an object after a break.

        This method should create a GraphicInterface and store it in
        ``self.interfaces``.

        Args:
            local_start_x: The local starting position of this
                drawing segment.
            start: The starting point in document space for drawing.

        Note: By default this is a no-op. Subclasses with with
            rendered appearances should override this.
        """

    def render_spanning_continuation(
        self, local_start_x: Unit, start: Point, stop: Point
    ):
        """
        Render the continuation of an object after a break and before another.

        For use in flowable containers when rendering an object that crosses
        two breaks. This function should render the portion of the object
        surrounded by breaks on either side.

        This method should create a GraphicInterface and store it in
        ``self.interfaces``.

        Args:
            local_start_x: The local starting position of this
                drawing segment.
            start: The starting point in document space for drawing.
            stop: The stopping point in document space for drawing.

        Note: By default this is a no-op. Subclasses with with
            rendered appearances should override this.
        """

    @staticmethod
    def _resolve_parent(value: Optional[PositionedObject]) -> PositionedObject:
        if value is None:
            return neoscore.document.pages[0]
        return value

    def _set_parent_and_register_self(self, value: Optional[PositionedObject]):
        if value is None:
            value = neoscore.document.pages[0]
        self._parent = value
        if hasattr(self._parent, "_register_child"):
            self._parent._register_child(self)

    def _register_child(self, child: PositionedObject):
        """Add an object to ``self.children``."""
        self.children.append(child)

    def _unregister_child(self, child: PositionedObject):
        """Remove an object from ``self.children``."""
        self.children.remove(child)
