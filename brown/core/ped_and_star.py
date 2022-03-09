from typing import Optional, cast

from brown.core.graphic_object import GraphicObject
from brown.core.mapping import Positioned
from brown.core.music_text import MusicText
from brown.core.object_group import ObjectGroup
from brown.core.spanner_2d import Spanner2D
from brown.core.staff_object import StaffObject
from brown.utils.point import Point, PointDef
from brown.utils.units import GraphicUnit


class PedAndStar(ObjectGroup, Spanner2D, StaffObject):

    """Pedal notation in the ornate 'Ped' and release star style."""

    def __init__(
        self,
        start: PointDef,
        start_parent: GraphicObject,
        end: PointDef,
        end_parent: Optional[GraphicObject] = None,
    ):
        """
        Args:
            start: The position of the start-pedal mark relative to `start_parent`.
            start_parent: Anchor for the start-pedal mark, which must be in a staff
                or a staff itself.
            end: The position of the release-pedal mark relative to `end_parent`.
            end_parent: An optional anchor for the release-pedal mark. If provided,
                this must be in the same staff as `start_parent`. Otherwise, this
                defaults to `self`.
        """
        ObjectGroup.__init__(self, start, start_parent)
        Spanner2D.__init__(
            self,
            end if isinstance(end, Point) else Point(*end),
            cast(Positioned, end_parent) if end_parent else self,
        )
        StaffObject.__init__(self, self.parent)

        # Add opening pedal mark
        # (GraphicObject init handles registration with ObjectGroup)
        self.depress_mark = MusicText(
            (GraphicUnit(0), GraphicUnit(0)), "keyboardPedalPed", parent=self
        )
        self.lift_mark = MusicText(
            self.end_pos, "keyboardPedalUp", parent=self.end_parent
        )
