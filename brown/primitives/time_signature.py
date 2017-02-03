from brown.core.object_group import ObjectGroup
from brown.core.music_text_object import MusicTextObject
from brown.primitives.staff_object import StaffObject
from brown.utils.point import Point


class TimeSignature(ObjectGroup, StaffObject):

    _glyphnames = {
        1: "timeSig1",
        2: "timeSig2",
        3: "timeSig3",
        4: "timeSig4",
        5: "timeSig5",
        6: "timeSig6",
        7: "timeSig7",
        8: "timeSig8",
        9: "timeSig9",
    }

    def __init__(self, position_x, duration, staff):
        """
        Args:
            position_x (StaffUnit): The x position relative to the
                parent staff
            duration (Duration): The length of a measure in this
                time signature. The numerator and denominators
                of this duration are used literally as the numbers
                in the rendered representation of the signature.
                While a 6/8 measure will take the same amount of time
                as a 3/4 measure, the representations (and note groupings)
                are different.
            staff (Staff): The parent staff
        """
        ObjectGroup.__init__(self, Point(position_x, staff.unit(0)),
                             parent=staff,
                             objects=None)
        StaffObject.__init__(self, staff)
        self._duration = duration
        # Add one glyph for each digit
        # TODO: This does not currently support multi-digit values
        #       so time signatures like 12/8 are not supported.
        #       this may be a good case for making a MusicTextObject
        #       as that would automatically be able to handle multi-line
        #       positioning, text centering, etc.
        self._numerator_glyph = MusicTextObject(
            (staff.unit(0), staff.unit(1)),
            self._glyphnames[self.duration.numerator],
            parent=self)
        self.register_object(self.numerator_glyph)
        self._denominator_glyph = MusicTextObject(
            (staff.unit(0), staff.unit(3)),
            self._glyphnames[self.duration.denominator],
            parent=self)
        self.register_object(self.denominator_glyph)

    ######## PUBLIC PROPERTIES ########

    @property
    def numerator_glyph(self):
        """MusicTextObject: The upper glyph for the time signature"""
        return self._numerator_glyph

    @property
    def denominator_glyph(self):
        """MusicTextObject: The lower glyph for the time signature"""
        return self._denominator_glyph

    @property
    def duration(self):
        """Duration: The length of one bar in this time signature"""
        return self._duration
