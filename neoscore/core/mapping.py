from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import Unit

if TYPE_CHECKING:
    from neoscore.core.positioned_object import PositionedObject


def map_between(src: PositionedObject, dst: PositionedObject) -> Point:
    """Find a Positioned object's logical position relative to another

    This calculates the position in *logical* space, which differs
    from canvas space in that it doesn't account for repositioning of
    objects inside ``Flowable`` containers. For example, this function
    will return the same relative position for two objects in a
    ``Flowable`` container whether or not they are separated by a line
    break.

    Args:
        src: The object to map from
        dst: The object to map to
    """
    # Handle easy cases
    if src == dst:
        return ORIGIN
    if src.parent == dst.parent:
        return dst.pos - src.pos
    if dst.parent == src:
        return dst.pos
    if src.parent == dst:
        return -src.pos
    # Start by collecting all ancestor using IDs because they're hashable
    src_ancestor_ids = set(id(obj) for obj in src.ancestors)
    relative_dst_pos = dst.pos
    for dst_ancestor in dst.ancestors:
        if hasattr(dst_ancestor, "parent"):
            relative_dst_pos += dst_ancestor.pos
        if id(dst_ancestor) in src_ancestor_ids:
            # Now find relative_src_pos and return relative_dst_pos - relative_src_pos
            relative_src_pos = src.pos
            for src_ancestor in src.ancestors:
                if hasattr(src_ancestor, "parent"):
                    relative_src_pos += src_ancestor.pos
                if src_ancestor == dst_ancestor:
                    return relative_dst_pos - relative_src_pos
            # Since we've already determined there is a common
            # ancestor, this should never happen
            assert False, "Unreachable"
    raise ValueError(f"{src} and {dst} have no common ancestor")


def map_between_x(src: PositionedObject, dst: PositionedObject) -> Unit:
    # TODO once main function is shown to work, copy here and edit as needed
    return map_between(src, dst).x


def descendant_pos(descendant: PositionedObject, ancestor: PositionedObject) -> Point:
    """Find the position of a descendant relative to one of its ancestors.

    Raises:
        ValueError: If ``ancestor`` is not an ancestor of ``descendant``
    """
    pos = descendant.pos
    for parent in descendant.ancestors:
        if parent == ancestor:
            return pos
        pos += parent.pos
    raise ValueError(f"{ancestor} is not an ancestor of {descendant}")


def descendant_pos_x(descendant: PositionedObject, ancestor: PositionedObject) -> Unit:
    """Find the x position of a descendant relative to one of its ancestors.

    This is a specialized version of ``descendant_pos`` provided for optimization.

    Raises:
        ValueError: If ``ancestor`` is not an ancestor of ``descendant``
    """
    pos_x = descendant.pos.x
    for parent in descendant.ancestors:
        if parent == ancestor:
            return pos_x
        pos_x += parent.pos.x
    raise ValueError(f"{ancestor} is not an ancestor of {descendant}")


def canvas_pos_of(obj: PositionedObject) -> Point:
    """Find the paged document position of a PositionedObject.

    Args:
        obj: Any object in the document.

    Returns: The object's paged position relative to the document.
    """
    pos = ORIGIN
    current = obj
    while hasattr(current, "parent"):
        pos += current.pos
        current = current.parent
        if hasattr(current, "map_to_canvas"):
            # Parent appears to be a flowable,
            # so let it decide where the point goes.
            return cast(Any, current).map_to_canvas(pos)
    return pos
