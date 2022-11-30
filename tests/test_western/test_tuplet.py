import pytest

from neoscore.core.directions import DirectionY
from neoscore.core.exceptions import MusicFontGlyphNotFoundError
from neoscore.core.point import ORIGIN, ZERO, Point
from neoscore.core.units import Mm, Unit
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

    def test_left_to_right_error_tuplet(self):
        with pytest.raises(AttributeError):
            Tuplet((Mm(0), Mm(0)), self.note3, (Mm(0), Mm(0)), self.note1, "3:2")

        try:
            Tuplet((Mm(0), Mm(0)), self.note1, (Mm(0), Mm(0)), self.note3, "3:2")
        except Exception as exc:
            assert False, f"Tuplet raised an exception {exc}"

    def test_incorrect_ratio_text_content(self):
        with pytest.raises(MusicFontGlyphNotFoundError):
            Tuplet(
                (Mm(0), Mm(0)), self.note1, (Mm(0), Mm(0)), self.note3, "Hello World"
            )

    def test_flat_tuplet_down_bracket(self):
        tuplet = Tuplet((Mm(0), Mm(0)), self.note1, (Mm(0), Mm(0)), self.note3, "3:2")
        assert tuplet.line_path.elements[0].pos == Point(x=Mm(0.0), y=Mm(0.0))
        assert tuplet.direction.value == 1
        assert tuplet.line_path.elements[1].pos == Point(
            x=Mm(0.0), y=self.staff.unit(1)
        )
        assert tuplet.end_parent == self.note3
        assert tuplet.line_path.elements[3].pos == Point(x=Mm(0.0), y=Mm(0.0))
        assert tuplet.end_pos == Point(x=Mm(0.0), y=Mm(0.0))
        assert tuplet.angle == 0
        assert tuplet.text_start_point == Point(x=Mm(5), y=Unit(4.961))

    def test_flat_tuplet_up_bracket(self):
        tuplet = Tuplet(
            (Mm(0), Mm(0)),
            self.note1,
            (Mm(0), Mm(0)),
            self.note3,
            "3:2",
            bracket_dir=DirectionY.UP,
        )
        assert tuplet.line_path.elements[0].pos == Point(x=Mm(0.0), y=Mm(0.0))
        assert tuplet.direction.value == -1
        assert tuplet.line_path.elements[1].pos == Point(
            x=Mm(0.0), y=self.staff.unit(-1)
        )
        assert tuplet.end_parent == self.note3
        assert tuplet.line_path.elements[3].pos == Point(x=Mm(0.0), y=Mm(0.0))
        assert tuplet.end_pos == Point(x=Mm(0.0), y=Mm(0.0))
        assert tuplet.angle == 0
        assert tuplet.text_start_point == Point(x=Mm(5), y=Unit(-4.961))

    def test_sloping_tuplet_up_bracket(self):
        tuplet = Tuplet(
            (Mm(0), Mm(0)),
            self.note1,
            (Mm(0), Mm(-10)),
            self.note3,
            "3:2",
            bracket_dir=DirectionY.UP,
        )
        assert tuplet.line_path.elements[0].pos == Point(x=Mm(0.0), y=Mm(0.0))
        assert tuplet.direction.value == -1
        assert tuplet.line_path.elements[1].pos == Point(
            x=Mm(0.0), y=self.staff.unit(-1)
        )
        assert tuplet.end_parent == self.note3
        assert tuplet.line_path.elements[3].pos == Point(x=Mm(0.0), y=Mm(-10.0))
        assert tuplet.end_pos == Point(x=Mm(0.0), y=Mm(-10.0))
        assert tuplet.angle == -45
        assert tuplet.text_start_point == Point(x=Mm(5), y=Unit(-19.134))

    def test_sloping_tuplet_down_bracket(self):
        tuplet = Tuplet((Mm(0), Mm(0)), self.note1, (Mm(0), Mm(-10)), self.note3, "3:2")
        assert tuplet.line_path.elements[0].pos == Point(x=Mm(0.0), y=Mm(0.0))
        assert tuplet.direction.value == 1
        assert tuplet.line_path.elements[1].pos == Point(
            x=Mm(0.0), y=self.staff.unit(1)
        )
        assert tuplet.end_parent == self.note3
        assert tuplet.line_path.elements[3].pos == Point(x=Mm(0.0), y=Mm(-10.0))
        assert tuplet.end_pos == Point(x=Mm(0.0), y=Mm(-10.0))
        assert tuplet.angle == -45
        assert tuplet.text_start_point == Point(x=Mm(5), y=Unit(-9.213))
