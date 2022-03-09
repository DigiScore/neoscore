from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, cast

from brown.core import mapping
from brown.core.graphic_object import GraphicObject
from brown.core.mapping import Positioned, first_ancestor_of_exact_class
from brown.utils.exceptions import NoAncestorStaffError
from brown.utils.point import Point
from brown.utils.units import Unit

if TYPE_CHECKING:
    from brown.core.staff import Staff


class StaffObject:

    """An object which must always be the descendant of a Staff

    This is a Mixin class, meant to be paired with GraphicObject classes.

    Usage within a GraphicObject will look something like:

    >>> class SomeMusicGlyph(MusicText, StaffObject):  # doctest: +SKIP
    ...     def __init__(self, ...):
    ...         MusicText.__init__(self, ...)
    ...         StaffObject.__init__(self, ...)
    """

    def __init__(self, parent: GraphicObject):
        self._staff = StaffObject.find_staff(cast(Positioned, parent))
        if not self._staff:
            raise NoAncestorStaffError

    ######## PUBLIC PROPERTIES ########

    @property
    def staff(self):
        """Staff: The staff associated with this object"""
        return self._staff

    @property
    def pos_in_staff(self) -> Point:
        """The logical position of this object relative to the staff."""
        return mapping.map_between(self.staff, cast(mapping.Positioned, self))

    @property
    def pos_x_in_staff(self) -> Unit:
        """A specialized version of `pos_in_staff` which only finds the x pos"""
        return mapping.map_between_x(self.staff, cast(mapping.Positioned, self))

    ######## PRIVATE METHODS ########

    @staticmethod
    def find_staff(obj: Positioned) -> Optional[Staff]:
        """Find the first staff which is an ancestor of `obj` or `obj` itself"""
        if type(obj).__name__ == "Staff":
            return cast(Any, obj)
        return first_ancestor_of_exact_class(obj, "Staff")
