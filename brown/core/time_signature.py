from brown.core.music_text import MusicText
from brown.core.object_group import ObjectGroup
from brown.core.staff_object import StaffObject
from brown.utils.point import Point


class TimeSignature(ObjectGroup, StaffObject):

    """A logical and graphical time signature

    TODO: Time signatures with differing character-length numerators and
    denominators (e.g. 12/8) currently display incorrectly as left-justified.
    """

    _glyph_names = {
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

    def __init__(self, pos_x, meter, staff):
        """
        Args:
            pos_x (StaffUnit): The x position relative to the
                parent staff
            meter (Beat): The length of a measure in this
                time signature. The numerator and denominators
                of this duration are used literally as the numbers
                in the rendered representation of the signature.
                While a 6/8 measure will take the same amount of time
                as a 3/4 measure, the representations (and note groupings)
                are different.
            staff (Staff): The parent staff
        """
        ObjectGroup.__init__(self, Point(pos_x, staff.unit(0)), staff)
        StaffObject.__init__(self, staff)
        self._meter = meter
        # Add one glyph for each digit
        self._numerator_glyph = MusicText(
            (staff.unit(0), staff.unit(1)),
            TimeSignature._glyphs_for_number(self.meter.numerator),
            self)
        self._denominator_glyph = MusicText(
            (staff.unit(0), staff.unit(3)),
            TimeSignature._glyphs_for_number(self.meter.denominator),
            self)

    ######## PUBLIC PROPERTIES ########

    @property
    def numerator_glyph(self):
        """MusicText: The upper glyph for the time signature"""
        return self._numerator_glyph

    @property
    def denominator_glyph(self):
        """MusicText: The lower glyph for the time signature"""
        return self._denominator_glyph

    @property
    def meter(self):
        """Beat: The length of one bar in this time signature"""
        return self._meter

    ######## PRIVATE METHODS  ########

    @staticmethod
    def _glyphs_for_number(number):
        """Convert a number to a list of SMuFL glyph names.

        Args:
            number (int): The time signature number to derive from

        Returns:
            list[str]: The time signature glyph names for the digits of `number`.
        """
        return [TimeSignature._glyph_names[int(digit)] for digit in str(number)]
