from brown.core.music_text import MusicText
from brown.core.object_group import ObjectGroup
from brown.core.staff import Staff
from brown.core.staff_object import StaffObject
from brown.models.beat import Beat
from brown.utils.point import Point
from brown.utils.units import Unit


class TimeSignature(ObjectGroup, StaffObject):

    """A logical and graphical time signature

    TODO LOW: Time signatures with differing character-length numerators and
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

    def __init__(self, pos_x: Unit, meter: Beat, staff: Staff):
        """
        Args:
            pos_x: The x position relative to the
                parent staff
            meter: The length of a measure in this
                time signature. The numerator and denominators
                of this duration are used literally as the numbers
                in the rendered representation of the signature.
                While a 6/8 measure will take the same amount of time
                as a 3/4 measure, the representations (and note groupings)
                are different.
            staff: The parent staff
        """
        ObjectGroup.__init__(self, Point(pos_x, staff.unit(0)), staff)
        StaffObject.__init__(self, staff)
        self._meter = meter
        # Add one glyph for each digit
        self._numerator_glyph = MusicText(
            (staff.unit(0), staff.unit(1)),
            TimeSignature._glyphs_for_number(self.meter.numerator),
            self,
        )
        self._denominator_glyph = MusicText(
            (staff.unit(0), staff.unit(3)),
            TimeSignature._glyphs_for_number(self.meter.denominator),
            self,
        )

    ######## PUBLIC PROPERTIES ########

    @property
    def numerator_glyph(self) -> MusicText:
        """MusicText: The upper glyph for the time signature"""
        return self._numerator_glyph

    @property
    def denominator_glyph(self) -> MusicText:
        """MusicText: The lower glyph for the time signature"""
        return self._denominator_glyph

    @property
    def meter(self) -> Beat:
        """Beat: The length of one bar in this time signature"""
        return self._meter

    ######## PRIVATE METHODS  ########

    @staticmethod
    def _glyphs_for_number(number: int) -> list[str]:
        """Convert time signature number to a list of SMuFL glyph names."""
        return [TimeSignature._glyph_names[int(digit)] for digit in str(number)]
