from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, cast

from neoscore.core import mapping
from neoscore.core.mapping import Positioned, first_ancestor_with_attr
from neoscore.core.positioned_object import PositionedObject
from neoscore.utils.exceptions import NoAncestorStaffError
from neoscore.utils.point import Point
from neoscore.utils.units import Unit

if TYPE_CHECKING:
    from neoscore.core.staff import Staff


class StaffObject:

    """An object which must always be the descendant of a Staff

    This is a Mixin class, meant to be paired with PositionedObject classes.

    Usage within a PositionedObject will look something like:

    >>> class SomeMusicGlyph(MusicText, StaffObject):  # doctest: +SKIP
    ...     def __init__(self, ...):
    ...         MusicText.__init__(self, ...)
    ...         StaffObject.__init__(self, ...)
    """

    def __init__(self, parent: PositionedObject):
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
        marker = "_neoscore_staff_type_marker"
        if hasattr(obj, marker):
            return cast(Any, obj)
        return first_ancestor_with_attr(obj, marker)
