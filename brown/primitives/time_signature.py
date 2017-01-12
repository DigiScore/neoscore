from brown.core.object_group import ObjectGroup
from brown.core.music_glyph import MusicGlyph
from brown.primitives.staff_object import StaffObject
from brown.utils.point import Point
from brown.models.duration import Duration


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

    def __init__(self, position_x, numerator, denominator, staff):
        """
        Args:
            position_x (StaffUnit): The x position relative to the
                parent staff
            numerator (int): The upper value of the time signature
            denominator (int): The lower value of the time signature
            staff (Staff): The parent staff
        """
        ObjectGroup.__init__(self, Point(position_x, staff.unit(0)),
                             parent=staff,
                             objects=None)
        StaffObject.__init__(self, staff)
        self._numerator = numerator
        self._denominator = denominator
        # Add one glyph for each digit
        # TODO: This does not currently support multi-digit values
        #       so time signatures like 12/8 are not supported.
        #       this may be a good case for making a MusicTextObject
        #       as that would automatically be able to handle multi-line
        #       positioning, text centering, etc.
        self._numerator_glyph = MusicGlyph((staff.unit(0), staff.unit(1)),
                                           self._glyphnames[self.numerator],
                                           parent=self)
        self.register_object(self.numerator_glyph)
        self._denominator_glyph = MusicGlyph((staff.unit(0), staff.unit(3)),
                                             self._glyphnames[self.denominator],
                                             parent=self)
        self.register_object(self.denominator_glyph)

    ######## PUBLIC PROPERTIES ########

    @property
    def numerator(self):
        """int: The numerical upper value of the time signature"""
        return self._numerator

    @property
    def denominator(self):
        """int: The numerical lower value of the time signature"""
        return self._denominator

    @property
    def numerator_glyph(self):
        """MusicGlyph: The upper glyph for the time signature"""
        return self._numerator_glyph

    @property
    def denominator_glyph(self):
        """MusicGlyph: The lower glyph for the time signature"""
        return self._denominator_glyph

    @property
    def duration(self):
        """Duration: The length of one bar in this time signature"""
        return Duration(self.numerator, self.denominator)
