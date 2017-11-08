from brown.core.music_text import MusicText
from brown.core.staff_object import StaffObject
from brown.models.beat import Beat
from brown.models.pitch import Pitch
from brown.utils.units import Mm


class Notehead(MusicText, StaffObject):

    """A simple notehead glyph whose appearance is determined by a Duration

    Currently, values larger than whole notes are not supported.
    """

    _glyphnames = {
        1024: 'noteheadBlack',
        512: 'noteheadBlack',
        256: 'noteheadBlack',
        128: 'noteheadBlack',
        64: 'noteheadBlack',
        32: 'noteheadBlack',
        16: 'noteheadBlack',
        8: 'noteheadBlack',
        4: 'noteheadBlack',
        2: 'noteheadHalf',
        1: 'noteheadWhole',
    }

    def __init__(self, pos_x, pitch, duration, parent):
        """
        Args:
            pos_x (Unit): The x-axis position relative to `parent`.
                The y-axis position is calculated automatically based
                on `pitch` and contextual information in `self.staff`.
            pitch (Pitch or str): May be a `str` pitch representation.
                See `Pitch` for valid signatures.
            duration (Beat or init tuple): The logical duration of
                the notehead. This is used to determine the glyph style.
            parent (GraphicObject): Must either be a `Staff` or an object
                with an ancestor `Staff`.
        """
        self._pitch = (pitch if isinstance(pitch, Pitch)
                       else Pitch(pitch))
        self._duration = (duration if isinstance(duration, Beat)
                          else Beat(*duration))
        # Use a temporary y-axis position before calculating it for real
        MusicText.__init__(self,
                           (pos_x, Mm(0)),
                           [self._glyphnames[self.duration.base_division]],
                           parent)
        StaffObject.__init__(self, parent)
        self.y = self.staff.unit(
            self.staff_pos
            - self.flowable.map_between_locally(self.staff, self.parent).y)

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
        return (self.staff.middle_c_at(self.pos_in_staff.x) +
                self.staff.unit(self.pitch.staff_pos_from_middle_c))
