import unittest

import pytest

from brown.core import brown
from brown.core.accidental import Accidental
from brown.core.clef import Clef
from brown.core.flowable import Flowable
from brown.core.music_char import MusicChar
from brown.core.staff import Staff
from brown.models.accidental_type import AccidentalType
from brown.utils.point import Point
from brown.utils.units import Mm


class TestAccidental(unittest.TestCase):
    def setUp(self):
        brown.setup()
        self.flowable = Flowable(Point(Mm(0), Mm(0)), Mm(10000), Mm(100))
        self.staff = Staff(Point(Mm(0), Mm(0)), Mm(100), self.flowable)
        Clef(self.staff, Mm(0), "treble")

    def test_canonical_name_mapping(self):
        acc = Accidental((Mm(0), Mm(0)), AccidentalType.sharp, self.staff)
        assert acc.music_chars == [MusicChar(self.staff.music_font, "accidentalSharp")]

        acc = Accidental((Mm(0), Mm(0)), AccidentalType.natural, self.staff)
        assert acc.music_chars == [
            MusicChar(self.staff.music_font, "accidentalNatural")
        ]

        acc = Accidental((Mm(0), Mm(0)), AccidentalType.sharp, self.staff)
        assert acc.music_chars == [MusicChar(self.staff.music_font, "accidentalSharp")]

    @pytest.mark.xfail
    def test_modifying_accidental_type_changes_music_char(self):
        # This will fail until the causing bug is fixed
        acc = Accidental((Mm(0), Mm(0)), AccidentalType.sharp, self.staff)
        acc.accidental_type = AccidentalType.flat
        assert acc.music_chars == [MusicChar(self.staff.music_font, "accidentalFlat")]
