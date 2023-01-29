import pytest

from neoscore.core.point import ORIGIN
from neoscore.core.units import ZERO, Mm
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff
from neoscore.western.tremolo import Tremolo

from ..helpers import AppTest


class TestTremolo(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff(ORIGIN, None, Mm(200))
        clef = Clef(ZERO, self.staff, "treble")
        self.cr1 = Chordrest(Mm(10), self.staff, ["c'"], (1, 2))
        self.cr2 = Chordrest(Mm(20), self.staff, ["d"], (1, 2))
        self.cr3 = Chordrest(Mm(30), self.staff, [], (1, 2))
        self.cr4 = Chordrest(Mm(40), self.staff, ["b,"], (1, 1))
        self.cr5 = Chordrest(Mm(50), self.staff, ["c"], (1, 8))
        self.cr6 = Chordrest(Mm(60), self.staff, ["f'"], (1, 8))
        self.cr7 = Chordrest(Mm(70), self.staff, ["c", "e", "g"], (1, 8))
        self.cr8 = Chordrest(Mm(80), self.staff, ["f'", "a'", "c''"], (1, 8))

    def test_init_with_int_indication_args(self):
        tremolo = Tremolo(ORIGIN, self.staff, 3)
        assert tremolo.parent == self.staff
        assert len(tremolo.music_chars) == 1
        assert tremolo.music_chars[0].glyph_info.canonical_name == "tremolo3"
        assert tremolo.pos.x == ZERO
        assert tremolo.pos.y == ZERO

    def test_init_with_smufl_indication_args(self):
        tremolo = Tremolo(ORIGIN, self.staff, "pendereckiTremolo")
        assert tremolo.parent == self.staff
        assert len(tremolo.music_chars) == 1
        assert tremolo.music_chars[0].glyph_info.canonical_name == "pendereckiTremolo"
        assert tremolo.pos.x == ZERO
        assert tremolo.pos.y == ZERO

    def test_init_build_with_for_chordrest_function(self):
        tremolo = Tremolo.for_chordrest(self.cr2, 3)
        assert tremolo.parent == self.cr2
        assert len(tremolo.music_chars) == 1
        assert tremolo.music_chars[0].glyph_info.canonical_name == "tremolo3"

    def test_init_with_invalid_stroke_count(self):
        with pytest.raises(ValueError):
            tremolo = Tremolo(ORIGIN, self.staff, 0)
        with pytest.raises(ValueError):
            tremolo = Tremolo(ORIGIN, self.staff, -1)
        with pytest.raises(ValueError):
            tremolo = Tremolo(ORIGIN, self.staff, 6)
