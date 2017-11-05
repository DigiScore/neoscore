from brown.core.music_text import MusicText
from brown.core.object_group import ObjectGroup
from brown.core.spanner import Spanner
from brown.core.staff_object import StaffObject
from brown.utils.units import GraphicUnit


class PedAndStar(ObjectGroup, Spanner, StaffObject):

    """Pedal notation in the ornate 'Ped' and release star style."""

    def __init__(self,
                 start, start_parent,
                 end, end_parent=None):
        """
        Args:
            start (Point or tuple init args): The position of the start-pedal
                mark relative to start_parent.
            start_parent (GraphicObject): An object either in a Staff or
                a staff itself. This object will become the line's parent.
            end (Point): The position of the release-pedal mark relative
                to end_parent (if provided).
            end_parent (GraphicObject): An object either in a Staff or
                a staff itself. The root staff of this *must* be the same
                as the root staff of `start_parent`. If omitted, the
                stop point is relative to the start point.
        """
        ObjectGroup.__init__(self, start, start_parent)
        Spanner.__init__(self, end, end_parent)
        StaffObject.__init__(self, self.parent)

        # Add opening pedal mark
        # (GraphicObject init handles registration with ObjectGroup)
        self.depress_mark = MusicText((GraphicUnit(0), GraphicUnit(0)),
                                      'keyboardPedalPed',
                                      parent=self)
        self.lift_mark = MusicText(self.end_pos,
                                   'keyboardPedalUp',
                                   parent=self.end_parent)
