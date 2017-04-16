import re

from brown.models.accidental_type import AccidentalType
from brown.utils.exceptions import InvalidPitchDescriptionError


class Pitch:

    """A pitch with a letter, octave, and accidental"""

    _pitch_regex = re.compile("^([a-g])([snf])?('*|,*)$")
    natural_pitch_classes = {
        'c': 0,
        'd': 2,
        'e': 4,
        'f': 5,
        'g': 7,
        'a': 9,
        'b': 11
    }
    _diatonic_degrees_in_c = {
        'c': 1,
        'd': 2,
        'e': 3,
        'f': 4,
        'g': 5,
        'a': 6,
        'b': 7
    }
    _middle_c_octave = 4
    _midi_middle_c = 60

    def __init__(self, pitch):
        """
        Valid pitch accidentals suffixes are `s` for sharp, `f` for flat,
        and `n` for explicit natural.

        Octaves are denoted by suffixes of commas or apostrophes,
        where none is C below middle-C, and each comma / apostrophe
        indicates an octave down or up, respectively.

        TODO: Explain better, needs examples - most users will not be
              familiar with lilypond pitch notation

        Args:
            pitch (str): A pitch representation of a string
                in lilypond notation

        """
        # These three are initialized by the pitch setter
        self._letter = None
        self._accidental_type = None
        self._octave = None
        self.pitch = pitch

    ######## SPECIAL METHODS ########

    def __repr__(self):
        """Represent the pitch as the code needed to instantiate it"""
        return '{}("{}")'.format(type(self).__name__, self.string_desriptor)

    def __eq__(self, other):
        """Two Pitches are equal if all of their attributes are equal

        Note that two pitches with the same midi number are not
        necessarily equal. Enharmonically equivalent pitches are
        not equal to each other.

            >>> Pitch("c") == Pitch("c")
            True
            >>> Pitch("c") == Pitch("bs,")
            False
            >>> Pitch("c").midi_number == Pitch("bs,").midi_number
            True
        """
        return (isinstance(other, type(self)) and
                self.letter == other.letter and
                self.accidental_type == other.accidental_type and
                self.octave == other.octave)

    def __hash__(self):
        """Hash based on the __repr__() of the Pitch.

        Pitches with different attributes will have different hashes"""
        return hash(self.__repr__())

    ######## PUBLIC PROPERTIES ########

    @property
    def pitch(self):
        """str: A string representation of the pitch.

        See `__init__` documentation for a complete description.
        """
        return self._pitch

    @pitch.setter
    def pitch(self, value):
        match = Pitch._pitch_regex.match(value)
        if match is None:
            raise InvalidPitchDescriptionError
        letter = match.group(1)
        accidental_str = match.group(2)
        ticks = match.group(3)
        self._letter = letter
        if accidental_str:
            self._accidental_type = AccidentalType[accidental_str]
        else:
            self._accidental_type = None
        if not ticks:
            self._octave = 3
        else:
            self._octave = 3 + (len(ticks) * (-1 if ticks[0] == ',' else 1))
        self._pitch = value

    @property
    def letter(self):
        """str: The a-g letter name of the pitch."""
        return self._letter

    @property
    def accidental_type(self):
        """AccidentalType or None: The accidental descriptor.

        If no accidental is needed for this pitch (e.g. C-natural in C Major),
        this should be left as `None`.
        """
        return self._accidental_type

    @property
    def octave(self):
        """int: The octave number for the pitch in scientific notation.

        `octave == 4` corresponds to middle-C.
        Descending pitches correspond to lower octave numbers.
        """
        return self._octave

    @property
    def pitch_class(self):
        """int: The 0-11 pitch class of this pitch."""
        natural = Pitch.natural_pitch_classes[self.letter]
        if self.accidental_type:
            return natural + self.accidental_type.value
        return natural

    @property
    def midi_number(self):
        """int: The midi pitch number, where A440 == 69 and middle C == 60"""
        return (Pitch._midi_middle_c +                           # Start point
                ((self.octave - Pitch._middle_c_octave) * 12) +  # 8ve offset
                self.pitch_class)                                # pitch offset

    @property
    def diatonic_degree_in_c(self):
        """int: The diatonic degree of the pitch as if it were in C.

            'c': 1,
            'd': 2,
            'e': 3,
            'f': 4,
            'g': 5,
            'a': 6,
            'b': 7
        """
        return Pitch._diatonic_degrees_in_c[self.letter]

    @property
    def staff_position_relative_to_middle_c(self):
        """float: The pitch's staff position relative to middle C.

        Values are in numeric pseudo-staff-units where positive
        values mean positions below middle C, and negative values
        mean positions above it.

        Examples:
            >>> Pitch("c'").staff_position_relative_to_middle_c
            0
            >>> Pitch("cs'").staff_position_relative_to_middle_c
            0
            >>> Pitch("d'").staff_position_relative_to_middle_c
            -0.5
            >>> Pitch("d''").staff_position_relative_to_middle_c
            -4
            >>> Pitch("cn,").staff_position_relative_to_middle_c
            7
        """
        middle_c = (4 * 7) + 1  # C at octave 4
        note_pos = (self.octave * 7) + self.diatonic_degree_in_c
        position = (note_pos - middle_c) / -2
        if position % 1 == 0:
            return int(position)
        else:
            return position

    @property
    def string_desriptor(self):
        """str: The string that can be used to recreate this Pitch"""
        descriptor = self.letter
        if self.accidental_type is not None:
            descriptor += self.accidental_type.name
        if self.octave > 3:
            descriptor += "'" * (self.octave - 3)
        elif self.octave < 3:
            descriptor += "," * (3 + (self.octave * -1))
        return descriptor
