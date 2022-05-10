from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, cast

from neoscore.core.exceptions import NoAncestorStaffError
from neoscore.core.point import Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import Unit

if TYPE_CHECKING:
    from neoscore.western.abstract_staff import AbstractStaff


class StaffObject:

    """An object which must always be the descendant of an :obj:`.AbstractStaff`.

    This is a mixin class for :obj:`.PositionedObject` classes.
    """

    def __init__(self, parent: PositionedObject):
        staff = StaffObject._find_staff(cast(PositionedObject, parent))
        if not staff:
            raise NoAncestorStaffError
        self._staff = staff

    @property
    def staff(self) -> AbstractStaff:
        """The ancestor staff"""
        return self._staff

    @property
    def pos_in_staff(self) -> Point:
        """The logical position of this object relative to the staff."""
        return self.staff.map_to(cast(PositionedObject, self))

    @property
    def pos_x_in_staff(self) -> Unit:
        """A specialized version of ``pos_in_staff`` which only finds the x pos"""
        return self.staff.map_x_to(cast(PositionedObject, self))

    @staticmethod
    def _find_staff(obj: PositionedObject) -> Optional[AbstractStaff]:
        """Find the first staff which is an ancestor of ``obj`` or ``obj`` itself"""
        marker = "_neoscore_abstract_staff_type_marker"
        if hasattr(obj, marker):
            return cast(Any, obj)
        return obj.first_ancestor_with_attr(marker)
