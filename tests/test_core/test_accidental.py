import unittest

import pytest

from neoscore.core import neoscore
from neoscore.core.accidental import Accidental
from neoscore.core.clef import Clef
from neoscore.core.flowable import Flowable
from neoscore.core.music_char import MusicChar
from neoscore.core.staff import Staff
from neoscore.models.accidental_type import AccidentalType
from neoscore.utils.point import Point
from neoscore.utils.units import Mm


class TestAccidental(unittest.TestCase):
    def setUp(self):
        neoscore.setup()
        self.flowable = Flowable(Point(Mm(0), Mm(0)), Mm(10000), Mm(100))
        self.staff = Staff(Point(Mm(0), Mm(0)), Mm(100), self.flowable)
        Clef(self.staff, Mm(0), "treble")

    def test_canonical_name_mapping(self):
        acc = Accidental((Mm(0), Mm(0)), AccidentalType.SHARP, self.staff)
        assert acc.music_chars == [MusicChar(self.staff.music_font, "accidentalSharp")]

        acc = Accidental((Mm(0), Mm(0)), AccidentalType.NATURAL, self.staff)
        assert acc.music_chars == [
            MusicChar(self.staff.music_font, "accidentalNatural")
        ]

        acc = Accidental((Mm(0), Mm(0)), AccidentalType.SHARP, self.staff)
        assert acc.music_chars == [MusicChar(self.staff.music_font, "accidentalSharp")]

    @pytest.mark.xfail
    def test_modifying_accidental_type_changes_music_char(self):
        # This will fail until the causing bug is fixed
        acc = Accidental((Mm(0), Mm(0)), AccidentalType.SHARP, self.staff)
        acc.accidental_type = AccidentalType.FLAT
        assert acc.music_chars == [MusicChar(self.staff.music_font, "accidentalFlat")]
