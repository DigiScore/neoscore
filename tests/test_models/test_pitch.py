import unittest

from nose.tools import assert_raises

from brown.models.pitch import Pitch, InvalidPitchDescriptionError


class TestPitch(unittest.TestCase):
    def test_pitch_init_common_case(self):
        pitch_string = 'af,,'
        test_pitch = Pitch(pitch_string)
        assert(test_pitch.pitch == pitch_string)
        assert(test_pitch.letter == 'a')
        assert(test_pitch.virtual_accidental.value == -1)
        assert(test_pitch.octave == 1)

    def test_pitch_init_no_letter_fails(self):
        with assert_raises(InvalidPitchDescriptionError):
            Pitch('s,')

    def test_no_octave_marks(self):
        assert(Pitch('af').octave == 3)

    def test_comma_octave_marks(self):
        assert(Pitch('af,').octave == 2)

    def test_apostrophe_octave_marks(self):
        assert(Pitch("af'").octave == 4)

    def test_pitch_class(self):
        assert(Pitch('af').pitch_class == 8)

    def test_midi_number(self):
        assert(Pitch("a''").midi_number == 81)
        assert(Pitch("a'").midi_number == 69)
        assert(Pitch("c'").midi_number == 60)
        assert(Pitch("cf").midi_number == 47)
        assert(Pitch("c").midi_number == 48)
        assert(Pitch("cn").midi_number == 48)
        assert(Pitch("cs").midi_number == 49)

    def test_diatonic_degree_in_c(self):
        # Simple identity test - mostly to raise a flag if the API changes
        degrees = {
            'c': 1,
            'd': 2,
            'e': 3,
            'f': 4,
            'g': 5,
            'a': 6,
            'b': 7
        }
        for letter, number in degrees.items():
            assert(Pitch(letter).diatonic_degree_in_c == number)

    def test_staff_position_relative_to_middle_c(self):
        assert(Pitch("c'").staff_position_relative_to_middle_c == 0)
        assert(Pitch("cs'").staff_position_relative_to_middle_c == 0)
        assert(Pitch("d'").staff_position_relative_to_middle_c == -0.5)
        assert(Pitch("d''").staff_position_relative_to_middle_c == -4)
        assert(Pitch("cn,").staff_position_relative_to_middle_c == 7)

    def test__eq__(self):
        assert(Pitch("c") == Pitch("c"))
        assert(Pitch("c,") == Pitch("c,"))
        assert(Pitch("cs,") == Pitch("cs,"))

    def test__ne__(self):
        assert(Pitch("c") != 'nonsense')
        assert(Pitch("c") != Pitch("d"))
        assert(Pitch("c") != Pitch("c,"))
        assert(Pitch("c") != Pitch("cs"))

    def test__hash__(self):
        self.assertEqual({Pitch("c"), Pitch("c"), Pitch("d")},
                         {Pitch("c"), Pitch("d")})
