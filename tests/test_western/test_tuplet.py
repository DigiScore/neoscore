import pytest

from neoscore.core.directions import DirectionY
from neoscore.core.exceptions import MusicFontGlyphNotFoundError
from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import ZERO, Mm, Unit
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff
from neoscore.western.tuplet import Tuplet

from ..helpers import AppTest


class TestTuplet(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff(ORIGIN, None, Mm(100))
        clef = Clef(ZERO, self.staff, "treble")

        self.note1 = Chordrest(Mm(5), self.staff, ["c"], (1, 8))
        self.note2 = Chordrest(Mm(10), self.staff, None, (1, 8))
        self.note3 = Chordrest(Mm(15), self.staff, ["d"], (1, 8))

    def test_incorrect_ratio_text_content(self):
        with pytest.raises(MusicFontGlyphNotFoundError):
            Tuplet(ORIGIN, self.note1, ORIGIN, self.note3, "Hello World")

    def test_flat_tuplet_down_bracket(self):
        tuplet = Tuplet(ORIGIN, self.note1, ORIGIN, self.note3, "3:2")
        assert tuplet.bracket.elements[0].pos == ORIGIN
        assert tuplet.direction.value == 1
        assert tuplet.bracket.elements[1].pos == Point(Mm(0.0), self.staff.unit(1))
        assert tuplet.end_parent == self.note3
        assert tuplet.bracket.elements[3].pos == ORIGIN
        assert tuplet.end_pos == ORIGIN
        assert tuplet.indicator.pos == Point(Mm(5), Unit(4.961))

    def test_flat_tuplet_up_bracket(self):
        tuplet = Tuplet(
            ORIGIN,
            self.note1,
            ORIGIN,
            self.note3,
            "3:2",
            bracket_dir=DirectionY.UP,
        )
        assert tuplet.bracket.elements[0].pos == ORIGIN
        assert tuplet.direction.value == -1
        assert tuplet.bracket.elements[1].pos == Point(Mm(0.0), self.staff.unit(-1))
        assert tuplet.end_parent == self.note3
        assert tuplet.bracket.elements[3].pos == ORIGIN
        assert tuplet.end_pos == ORIGIN
        assert tuplet.indicator.pos == Point(Mm(5), Unit(-4.961))

    def test_sloping_tuplet_up_bracket(self):
        tuplet = Tuplet(
            ORIGIN,
            self.note1,
            (Mm(0), Mm(-10)),
            self.note3,
            "3:2",
            bracket_dir=DirectionY.UP,
        )
        assert tuplet.bracket.elements[0].pos == ORIGIN
        assert tuplet.direction.value == -1
        assert tuplet.bracket.elements[1].pos == Point(Mm(0.0), self.staff.unit(-1))
        assert tuplet.end_parent == self.note3
        assert tuplet.bracket.elements[3].pos == Point(Mm(0.0), Mm(-10.0))
        assert tuplet.end_pos == Point(Mm(0.0), Mm(-10.0))
        assert tuplet.indicator.pos == Point(Mm(5), Unit(-19.134))

    def test_sloping_tuplet_down_bracket(self):
        tuplet = Tuplet(ORIGIN, self.note1, (Mm(0), Mm(-10)), self.note3, "3:2")
        assert tuplet.bracket.elements[0].pos == ORIGIN
        assert tuplet.direction.value == 1
        assert tuplet.bracket.elements[1].pos == Point(Mm(0.0), self.staff.unit(1))
        assert tuplet.end_parent == self.note3
        assert tuplet.bracket.elements[3].pos == Point(Mm(0.0), Mm(-10.0))
        assert tuplet.end_pos == Point(Mm(0.0), Mm(-10.0))
        assert tuplet.indicator.pos == Point(Mm(5), Unit(-9.213))

    def test_no_bracket(self):
        tuplet = Tuplet(ORIGIN, self.note1, ORIGIN, self.note3, include_bracket=False)
        assert tuplet.bracket is None
