from neoscore.core.flowable import Flowable
from neoscore.core.music_char import MusicChar
from neoscore.core.point import Point
from neoscore.core.units import Mm
from neoscore.western.accidental import Accidental
from neoscore.western.accidental_type import AccidentalType
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff

from ..helpers import AppTest


class TestAccidental(AppTest):
    def setUp(self):
        super().setUp()
        self.flowable = Flowable(Point(Mm(0), Mm(0)), None, Mm(10000), Mm(100))
        self.staff = Staff(Point(Mm(0), Mm(0)), self.flowable, Mm(100))
        Clef(Mm(0), self.staff, "treble")

    def test_canonical_name_mapping(self):
        acc = Accidental((Mm(0), Mm(0)), self.staff, AccidentalType.SHARP)
        assert acc.music_chars == [MusicChar(self.staff.music_font, "accidentalSharp")]

    def test_modifying_accidental_type_changes_music_char(self):
        # This will fail until the causing bug is fixed
        acc = Accidental((Mm(0), Mm(0)), self.staff, AccidentalType.SHARP)
        acc.accidental_type = AccidentalType.FLAT
        assert acc.music_chars == [MusicChar(self.staff.music_font, "accidentalFlat")]

    def test_extended_glyph_use(self):
        acc = Accidental((Mm(0), Mm(0)), self.staff, "accidentalQuarterToneSharpStein")
        assert acc.music_chars == [
            MusicChar(self.staff.music_font, "accidentalQuarterToneSharpStein")
        ]
