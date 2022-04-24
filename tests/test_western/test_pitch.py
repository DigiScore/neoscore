import unittest

import pytest

from neoscore.western.accidental_type import AccidentalType
from neoscore.western.pitch import InvalidPitchDescriptionError, Pitch


class TestPitch(unittest.TestCase):
    def test_pitch_from_str_common_case(self):
        assert Pitch.from_str("af,,") == Pitch("a", AccidentalType.FLAT, 2)

    def test_pitch_from_str_no_letter_fails(self):
        with pytest.raises(InvalidPitchDescriptionError):
            Pitch.from_str("s,")

    def test_no_octave_marks(self):
        assert Pitch.from_str("af") == Pitch("a", AccidentalType.FLAT, 4)

    def test_comma_octave_marks(self):
        assert Pitch.from_str("af,,,") == Pitch("a", AccidentalType.FLAT, 1)

    def test_apostrophe_octave_marks(self):
        assert Pitch.from_str("af''") == Pitch("a", AccidentalType.FLAT, 6)

    def test_accidental_variants(self):
        assert Pitch.from_str("gs") == Pitch("g", AccidentalType.SHARP, 4)
        assert Pitch.from_str("g#") == Pitch("g", AccidentalType.SHARP, 4)
        assert Pitch.from_str("gn") == Pitch("g", AccidentalType.NATURAL, 4)
        assert Pitch.from_str("gf") == Pitch("g", AccidentalType.FLAT, 4)
        assert Pitch.from_str("gb") == Pitch("g", AccidentalType.FLAT, 4)
        assert Pitch.from_str("gx") == Pitch("g", AccidentalType.DOUBLE_SHARP, 4)
        assert Pitch.from_str("gss") == Pitch("g", AccidentalType.DOUBLE_SHARP, 4)
        assert Pitch.from_str("gff") == Pitch("g", AccidentalType.DOUBLE_FLAT, 4)
        assert Pitch.from_str("gbb") == Pitch("g", AccidentalType.DOUBLE_FLAT, 4)

    def test_str_accidental(self):
        assert Pitch("a", "test", 3).accidental == "test"

    def test_diatonic_degree_in_c(self):
        assert Pitch.from_str("c").diatonic_degree_in_c == 1
        assert Pitch.from_str("d").diatonic_degree_in_c == 2
        assert Pitch.from_str("e").diatonic_degree_in_c == 3
        assert Pitch.from_str("f").diatonic_degree_in_c == 4
        assert Pitch.from_str("g").diatonic_degree_in_c == 5
        assert Pitch.from_str("a").diatonic_degree_in_c == 6
        assert Pitch.from_str("b").diatonic_degree_in_c == 7

    def test_staff_position_relative_to_middle_c(self):
        assert Pitch.from_str("c").staff_pos_from_middle_c == 0
        assert Pitch.from_str("cs").staff_pos_from_middle_c == 0
        assert Pitch.from_str("d").staff_pos_from_middle_c == -0.5
        assert Pitch.from_str("d'").staff_pos_from_middle_c == -4
        assert Pitch.from_str("cn,,").staff_pos_from_middle_c == 7

    def test_from_def_with_pitch(self):
        p = Pitch.from_str("c")
        assert Pitch.from_def(p) == p

    def test_from_def_with_str(self):
        assert Pitch.from_def("c") == Pitch.from_str("c")

    def test_from_def_with_tuple(self):
        assert Pitch.from_def(("g", AccidentalType.SHARP, 3)) == Pitch.from_str("g#,")
