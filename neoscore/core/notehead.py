from neoscore.core.mapping import map_between
from neoscore.core.music_text import MusicText
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.staff_object import StaffObject
from neoscore.models.beat import Beat, BeatDef
from neoscore.models.pitch import Pitch, PitchDef
from neoscore.utils.units import ZERO, Unit


class Notehead(MusicText, StaffObject):

    """A simple notehead glyph whose appearance is determined by a Duration

    Currently, values larger than whole notes are not supported.
    """

    _glyphnames = {
        1024: "noteheadBlack",
        512: "noteheadBlack",
        256: "noteheadBlack",
        128: "noteheadBlack",
        64: "noteheadBlack",
        32: "noteheadBlack",
        16: "noteheadBlack",
        8: "noteheadBlack",
        4: "noteheadBlack",
        2: "noteheadHalf",
        1: "noteheadWhole",
    }

    def __init__(
        self, pos_x: Unit, parent: PositionedObject, pitch: PitchDef, duration: BeatDef
    ):
        """
        Args:
            pos_x: The x-axis position relative to `parent`.
                The y-axis position is calculated automatically based
                on `pitch` and contextual information in `self.staff`.
            parent: Must either be a `Staff` or an object
                with an ancestor `Staff`.
            pitch: May be a `str` pitch representation.
                See `Pitch` for valid signatures.
            duration: The logical duration of
                the notehead. This is used to determine the glyph style.
        """
        self._pitch = Pitch.from_def(pitch)
        self._duration = Beat.from_def(duration)
        # Use a temporary y-axis position before calculating it for real
        MusicText.__init__(
            self, (pos_x, ZERO), parent, [self._glyphnames[self.duration.base_division]]
        )
        StaffObject.__init__(self, parent)
        self.y = self.staff.unit(
            self.staff_pos - map_between(self.staff, self.parent).y
        )

    ######## PUBLIC PROPERTIES ########

    @property
    def visual_width(self):
        """Unit: The visual width of the Notehead"""
        return self.bounding_rect.width

    @property
    def pitch(self):
        """Pitch: The logical pitch.

        May be set to a valid string pitch descriptor.
        See Pitch docs.
        """
        return self._pitch

    @pitch.setter
    def pitch(self, value):
        self._pitch = value

    @property
    def duration(self):
        """Beat: The time duration of this Notehead"""
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def staff_pos(self):
        """StaffUnit: The y-axis position in the staff.

        `StaffUnit(0)` means the top staff line, higher values
        mean lower pitches, and vice versa.
        """
        return self.staff.middle_c_at(self.pos_x_in_staff) + self.staff.unit(
            self.pitch.staff_pos_from_middle_c
        )
