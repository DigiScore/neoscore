from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any, List, Optional, Set, Type, cast

from backports.cached_property import cached_property

from neoscore.core import neoscore
from neoscore.core.point import ORIGIN, Point, PointDef
from neoscore.core.units import ZERO, Unit
from neoscore.interface.invisible_object_interface import InvisibleObjectInterface
from neoscore.interface.positioned_object_interface import PositionedObjectInterface

if TYPE_CHECKING:
    # Used in type annotations, imported here to avoid cyclic imports
    from neoscore.core.flowable import Flowable
    from neoscore.core.layout_controllers import NewLine


class render_cached_property(cached_property):  # noqa

    """A property annotation for fields which can be cached at render time.

    You can annotate any ``PositionedObject`` property to get this behavior, including
    on inheriting classes. ::

        class Example(PositionedObject):
            @render_cached_property
            def some_expensive_computed_property(self):
                ...

    Such properties must be immutable during rendering. Typical ``@property`` setters
    are not supported.
    """

    # Note that this class extends `cached_property`, but this is just a hack to make
    # Sphinx and other tools treat it like a property.

    def __init__(self, func):
        """
        :meta private:
        """
        self.func = func
        self.attrname = None
        self.__doc__ = func.__doc__

    def __get__(self, obj, cls):  # noqa
        if obj is None:
            return self
        result = self.func(obj)
        if not getattr(obj, "_currently_rendering", None):
            return result
        property_name = self.func.__name__
        value = obj.__dict__[property_name] = result
        obj._render_cached_properties.add(property_name)  # noqa
        return value

    def __set__(self, obj, val):
        raise AttributeError(f"can't set attribute '{self.func.__name__}'")


class PositionedObject:
    """An object positioned in the scene

    This is the base class of all objects in the neoscore scene tree.

    A single ``PositionedObject`` can have multiple graphical representations derived at
    render-time. If the object's ancestor is a :obj:`.Flowable`, it will be rendered as a
    flowable object, capable of being wrapped around lines.

    The position of this object is relative to that of its parent. Each ``PositionedObject``
    has another ``PositionedObject`` for a parent, except :obj:`.Page` objects, whose parent is
    always the global root :obj:`.Document`.

    For convenience, the parent may be initialized to ``None`` to indicate the first page of
    the document.

    To place objects directly in the scene on pages other than the first, simply set the
    parent to the desired page, accessed through the global document with
    ``neoscore.document.pages[n]``
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
    ):
        """
        Args:
            pos: The position of the object relative to its parent
            parent: The parent object. Defaults to the document's first page.
        """
        self.pos = pos
        self._children: List[PositionedObject] = []
        self._parent = PositionedObject._resolve_parent(parent)
        self._set_parent_and_register_self(parent)
        self._render_cached_properties: Set[str] = set()
        self._currently_rendering = False
        self._interfaces = []
        self._interface_for_children = None
        self._scale = 1.0
        self._rotation = 0.0
        self.transform_origin = ORIGIN

    @property
    def pos(self) -> Point:
        """The position of the object relative to its parent."""
        return self._pos

    @pos.setter
    def pos(self, value: PointDef):
        self._pos = Point.from_def(value)

    @property
    def scale(self) -> float:
        """A scale factor to be applied to the rendered object.

        Outside flowable contexts, scaling is inherited by children.

        Scaling occurs relative to ``self.transform_origin``, which is by default the
        local origin.
        """
        return self._scale

    @scale.setter
    def scale(self, value: float):
        self._scale = value

    @property
    def rotation(self) -> float:
        """A rotation angle in degrees.

        Outside flowable contexts, rotation is inherited by children.

        Rotation occurs relative to ``self.transform_origin``, which is by default the
        local origin.
        """
        return self._rotation

    @rotation.setter
    def rotation(self, value: float):
        self._rotation = value

    @property
    def transform_origin(self) -> Point:
        """The origin point for rotation and scaling transforms"""
        return self._transform_origin

    @transform_origin.setter
    def transform_origin(self, value: PointDef):
        self._transform_origin = Point.from_def(value)

    @property
    def x(self) -> Unit:
        """The x position of the object relative to its parent."""
        return self.pos.x

    @x.setter
    def x(self, value: Unit):
        self.pos = Point(value, self.y)

    @property
    def y(self) -> Unit:
        """The y position of the object relative to its parent."""
        return self.pos.y

    @y.setter
    def y(self, value: Unit):
        self.pos = Point(self.x, value)

    @property
    def breakable_length(self) -> Unit:
        """The breakable length of the object.

        This is used to determine how and where rendering cuts should be made. A length
        of zero indicates that no rendering cuts will be made.

        The default implementation of this method returns ``ZERO``. Subclasses which
        want to support flowable line breaks should override this method.
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
    def children(self) -> List[PositionedObject]:
        """All direct children of this object."""
        return self._children

    @children.setter
    def children(self, value: List[PositionedObject]):
        self._children = value

    @property
    def descendants(self) -> Iterator[PositionedObject]:
        """All the objects in the children subtree.

        This recursively searches all the object's children
        (and their children, etc.) and provides an iterator over them.

        The current implementation performs a simple recursive DFS over
        the tree, and has the potential to be rather slow.
        """
        for child in self.children:
            for subchild in child.descendants:
                yield subchild
            yield child

    @render_cached_property
    def flowable(self) -> Optional[Flowable]:
        """The flowable this object belongs in."""
        return cast(
            Any, self.first_ancestor_with_attr("_neoscore_flowable_type_marker")  # noqa
        )

    @property
    def interfaces(self) -> List[PositionedObjectInterface]:
        """The graphical backend binding interfaces for this object

        Interface objects are created and stored here upon calling :obj:`.render`.

        Typically each ``PositionedObject`` will have at most one interface for each
        flowable line it appears in.
        """
        return self._interfaces

    @property
    def interface_for_children(self) -> Optional[PositionedObjectInterface]:
        """The low level object interface to be used by children objects.

        Outside flowable contexts, interface classes utilize a parenting scheme much
        like core classes. The interfaces of child objects should use this field as
        their parent for proper position and transform inheritance.

        Users should rarely, if ever, have to deal with this field.
        """
        return self._interface_for_children

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

    @property
    def ancestors(self) -> Iterator[PositionedObject]:
        """All ancestors of this object.

        Follows the chain of parents up to and including the :obj:`.Document` root.

        The order begins with ``self.parent`` and traverses upward in the document tree.
        """
        ancestor = self.parent
        while True:
            yield ancestor
            if not hasattr(ancestor, "parent"):
                # Document root found
                break
            ancestor = ancestor.parent

    def first_ancestor_with_attr(self, attr: str) -> Optional[PositionedObject]:
        """Find this object's closest ancestor with an attribute"""
        return next(
            (item for item in self.ancestors if hasattr(item, attr)),
            None,
        )

    def descendant_pos(self, descendant: PositionedObject) -> Point:
        """Find the position of a descendant relative to this object.

        Raises:
            ValueError:
                If ``descendant`` is not a descendant of this object.
        """
        pos = descendant.pos
        for parent in descendant.ancestors:
            if parent == self:
                return pos
            pos += parent.pos
        raise ValueError(f"{self} is not an ancestor of {descendant}")

    def descendant_pos_x(self, descendant: PositionedObject) -> Unit:
        """Find the x position of a descendant relative to this object.

        This is a specialized version of ``descendant_pos`` provided for optimization.

        Raises:
            ValueError:
                If ``descendant`` is not a descendant of this object.
        """
        pos_x = descendant.pos.x
        for parent in descendant.ancestors:
            if parent == self:
                return pos_x
            pos_x += parent.pos.x
        raise ValueError(f"{self} is not an ancestor of {descendant}")

    def map_to(self, dst: PositionedObject) -> Point:
        """Find an object's logical position relative to this one

        This calculates the position in *logical* space, which differs from canvas space
        in that it doesn't account for repositioning of objects inside :obj:`.Flowable`
        containers. For example, this function will return the same relative position
        for two objects in a ``Flowable`` container whether they are separated by
        a line break.
        """
        # When changing this method be sure to make the equivalent change in `map_x_to`
        # Handle easy cases
        if self == dst:
            return ORIGIN
        if self.parent == dst.parent:
            return dst.pos - self.pos
        if dst.parent == self:
            return dst.pos
        if self.parent == dst:
            return -self.pos
        # Start by collecting all ancestor using IDs because they're hashable
        self_ancestor_ids = set(id(obj) for obj in self.ancestors)
        relative_dst_pos = dst.pos
        for dst_ancestor in dst.ancestors:
            if hasattr(dst_ancestor, "parent"):
                relative_dst_pos += dst_ancestor.pos
            if id(dst_ancestor) in self_ancestor_ids:
                # Now find relative_self_pos and return relative_dst_pos - relative_self_pos
                relative_self_pos = self.pos
                for self_ancestor in self.ancestors:
                    if hasattr(self_ancestor, "parent"):
                        relative_self_pos += self_ancestor.pos
                    if self_ancestor == dst_ancestor:
                        return relative_dst_pos - relative_self_pos
                # Since we've already determined there is a common
                # ancestor, this should never happen
                assert False, "Unreachable"
        raise ValueError(f"{self} and {dst} have no common ancestor")

    def map_x_to(self, dst: PositionedObject) -> Unit:
        """Like :obj:`.map_to`, but only return the X distance from to ``dst``."""

        # This implementation is copied from `map_to` and tweaked to only handle the X
        # axis. This is a very common operation, so this optimization is useful.

        # Handle easy cases
        if self == dst:
            return ZERO
        if self.parent == dst.parent:
            return dst.x - self.x
        if dst.parent == self:
            return dst.x
        if self.parent == dst:
            return -self.x
        # Start by collecting all ancestor using IDs because they're hashable
        self_ancestor_ids = set(id(obj) for obj in self.ancestors)
        relative_dst_x = dst.x
        for dst_ancestor in dst.ancestors:
            if hasattr(dst_ancestor, "parent"):
                relative_dst_x += dst_ancestor.x
            if id(dst_ancestor) in self_ancestor_ids:
                # Now find relative_self_x and return relative_dst_x - relative_self_x
                relative_self_x = self.x
                for self_ancestor in self.ancestors:
                    if hasattr(self_ancestor, "parent"):
                        relative_self_x += self_ancestor.x
                    if self_ancestor == dst_ancestor:
                        return relative_dst_x - relative_self_x
                # Since we've already determined there is a common
                # ancestor, this should never happen
                assert False, "Unreachable"
        raise ValueError(f"{self} and {dst} have no common ancestor")

    def canvas_pos(self) -> Point:
        """Find the document-space position of this object.

        For objects in :obj:`.Flowable`\ s, this should only be accessed at render time,
        when flowable layouts are available.
        """
        pos = ORIGIN
        current = self
        while hasattr(current, "parent"):
            pos += current.pos
            current = current.parent
            if hasattr(current, "map_to_canvas"):
                # Parent appears to be a flowable,
                # so let it decide where the point goes.
                return cast(Any, current).map_to_canvas(pos)
        return pos

    def remove(self):
        """Remove this object from the document tree."""
        if self.parent:
            self.parent.children.remove(self)

    def pre_render_hook(self):
        """Run code once just before document rendering begins.

        Implementations *must* call the superclass function as well.
        """
        self._currently_rendering = True

    def post_render_hook(self):
        """Run code once after document rendering completes.

        Implementations *must* call the superclass function as well.
        """
        for cached_property in self._render_cached_properties:
            del self.__dict__[cached_property]
        self._render_cached_properties.clear()
        self._currently_rendering = False

    def render(self):
        """Render the object and all its children.

        This and other render methods should generally not be called directly.
        """
        if self.flowable is not None:
            self.render_in_flowable()
        else:
            self._interface_for_children = InvisibleObjectInterface(
                self.pos,
                # Hack because root document obj lacks this property
                getattr(self.parent, "interface_for_children", None),
                self.scale,
                self.rotation,
                self.transform_origin,
            )
            self._interface_for_children.render()
            self.render_complete(self.pos)
        for child in self.children:
            child.render()

    def render_in_flowable(self):
        """Render the object to the scene, dispatching partial rendering calls
        when needed if an object flows across a break in the flowable.

        This and other render methods should generally not be called directly.
        """
        # Calculate position within flowable
        assert self.flowable is not None
        pos_in_flowable = self.flowable.descendant_pos(self)
        first_line_i = self.flowable.last_break_index_at(pos_in_flowable.x)
        first_line = self.flowable.lines[first_line_i]
        first_line_length = (
            first_line.flowable_x + first_line.length - pos_in_flowable.x
        )
        remaining_x = self.breakable_length - first_line_length
        if remaining_x <= ZERO:
            self.render_complete(self.canvas_pos(), first_line, pos_in_flowable.x)
            return

        # Render before break
        if first_line_length < Unit(1):
            # If a break-spanning object starts very close to its first line end,
            # skip that line.
            first_line_i += 1
            first_line = self.flowable.lines[first_line_i]
            first_line_length = (
                first_line.flowable_x + first_line.length - pos_in_flowable.x
            )
            remaining_x = self.breakable_length - first_line_length
        line_pos = first_line.canvas_pos()
        render_start_pos = Point(
            line_pos.x + (pos_in_flowable.x - first_line.flowable_x),
            line_pos.y + pos_in_flowable.y,
        )
        self.render_before_break(render_start_pos, first_line, pos_in_flowable.x)

        # Iterate through remaining length
        for current_line_i in range(first_line_i + 1, len(self.flowable.lines)):
            current_line = self.flowable.lines[current_line_i]
            line_pos = current_line.canvas_pos()
            render_start_pos = Point(line_pos.x, line_pos.y + pos_in_flowable.y)
            local_object_x = self.breakable_length - remaining_x
            if remaining_x > current_line.length:
                # Render spanning continuation
                self.render_spanning_continuation(
                    render_start_pos, current_line, local_object_x
                )
                remaining_x -= current_line.length
            else:
                # Render end
                self.render_after_break(render_start_pos, current_line, local_object_x)
                break

    def render_complete(
        self,
        pos: Point,
        flowable_line: Optional[NewLine] = None,
        flowable_x: Optional[Unit] = None,
    ):
        """Render the entire object.

        This is used to render all objects outside flowables, as well as those inside
        flowables when they fit completely in one line of the flowable.

        By default, this is a no-op. Subclasses with rendered appearances should
        override this.

        This method behaves differently inside and outside of flowables. Whether this
        object is inside a flowable can be determined by whether a ``flowable_line`` is
        given. When inside a flowable, the given position is in global document
        coordinates, and created interfaces (or higher level classes) must not be
        assigned a parent. When not inside a flowable, the given position is relative to
        ``self.parent`` and created interfaces (or higher level classes) must be
        assigned a parent. In this case, created interfaces should use
        ``self.parent.interface_for_children`` as their parent.

        This and other render methods should generally not be called directly.

        Args:
            pos: The rendering position. If outside a flowable, this is relative to
                the parent. Otherwise, it is in document coordinates.
            flowable_line: If in a ``Flowable``, the line in which this object appears
            flowable_x: If in a ``Flowable``, the flowable x position of this render

        """

    def render_before_break(self, pos: Point, flowable_line: NewLine, flowable_x: Unit):
        """Render the beginning of the object up to a stopping point.

        For use in flowable containers when rendering an object that crosses a line or
        page break. This function should render the beginning portion of the object up
        to the break.

        By default, this is a no-op. Subclasses with rendered appearances should
        override this.

        Created interfaces and higher level objects should not be assigned a parent.

        This and other render methods should generally not be called directly.

        Args:
            pos: The rendering position in document space for drawing.
            flowable_line: The line in which this object appears
            flowable_x: The flowable x position of this render

        """

    def render_spanning_continuation(
        self, pos: Point, flowable_line: NewLine, object_x: Unit
    ):
        """
        Render the continuation of an object after a break and before another.

        For use in flowable containers when rendering an object that crosses
        two breaks. This function should render the portion of the object
        surrounded by breaks on either side.

        By default, this is a no-op. Subclasses with rendered appearances should
        override this.

        Created interfaces and higher level objects should not be assigned a parent.

        This and other render methods should generally not be called directly.

        Args:
            pos: The rendering position in document space for drawing.
            flowable_line: The line in which this object appears
            object_x: The local object x position of the line's start.
        """

    def render_after_break(self, pos: Point, flowable_line: NewLine, object_x: Unit):
        """Render the continuation of an object after a break.

        For use in flowable containers when rendering an object that crosses a line or
        page break. This function should render the ending portion of an object after a
        break.

        By default, this is a no-op. Subclasses with rendered appearances should
        override this.

        Created interfaces and higher level objects should not be assigned a parent.

        This and other render methods should generally not be called directly.

        Args:
            pos: The rendering position in document space for drawing.
            flowable_line: The line in which this object appears
            object_x: The local object x position of the line's start.
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
