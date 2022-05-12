import pytest

from neoscore.core.brush import Brush
from neoscore.core.directions import DirectionY
from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Mm, Unit
from neoscore.western.arpeggio_line import ArpeggioLine
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.staff import Staff
from tests.helpers import AppTest


@pytest.mark.skipif("not AppTest.running_on_linux()")
class TestArpeggioLine(AppTest):
    def setUp(self):
        super().setUp()

    def test_arpeggio_line_init(self):
        font = MusicFont("Bravura", Mm)
        bottom_parent = PositionedObject((Mm(0), Mm(0)), None)
        top_parent = PositionedObject((Mm(0), Mm(-20)), None)

        arp = ArpeggioLine(
            (Mm(-1), Mm(-2)),
            bottom_parent,
            (Mm(1), Mm(2)),
            top_parent,
            True,
            font,
            "#ff0000",
            "#00ff00",
            "#0000ff",
        )
        assert len(arp.music_chars) == 13
        assert arp.music_chars[0] == MusicChar(font, "wiggleArpeggiatoUp")
        assert arp.music_chars[-1] == MusicChar(font, "wiggleArpeggiatoUpArrow")
        assert arp.brush == Brush("#ff0000")
        assert arp.pen == Pen("#00ff00")
        assert arp.background_brush == Brush("#0000ff")

    def test_for_chord_with_arrow_up(self):
        staff = Staff(ORIGIN, None, Mm(40))
        Clef(ZERO, staff, "treble")
        c = Chordrest(Mm(15), staff, ["c", "g", "eb'"], (1, 16))
        line = ArpeggioLine.for_chord(c, DirectionY.UP)
        assert line.parent == c
        assert line.end_parent == c
        assert line.pos == Point(Unit(-15.681), Unit(29.043))
        assert line.end_pos == Point(Unit(-15.681), Unit(-1.76))
        assert (
            line.music_chars[-1].glyph_info.canonical_name == "wiggleArpeggiatoUpArrow"
        )

    def test_for_chord_with_arrow_down(self):
        staff = Staff(ORIGIN, None, Mm(40))
        Clef(ZERO, staff, "treble")
        c = Chordrest(Mm(15), staff, ["c", "g", "eb'"], (1, 16))
        line = ArpeggioLine.for_chord(c, DirectionY.DOWN)
        assert line.parent == c
        assert line.end_parent == c
        assert line.pos == Point(Unit(-15.681), Unit(-1.76))
        assert line.end_pos == Point(Unit(-15.681), Unit(29.043))
        assert (
            line.music_chars[-1].glyph_info.canonical_name == "wiggleArpeggiatoUpArrow"
        )

    def test_for_chord_with_no_arrow(self):
        staff = Staff(ORIGIN, None, Mm(40))
        Clef(ZERO, staff, "treble")
        c = Chordrest(Mm(15), staff, ["c", "g", "eb'"], (1, 16))
        line = ArpeggioLine.for_chord(c)
        assert line.parent == c
        assert line.end_parent == c
        assert line.pos == Point(Unit(-15.681), Unit(-1.76))
        assert line.end_pos == Point(Unit(-15.681), Unit(29.043))
        assert line.music_chars[-1].glyph_info.canonical_name == "wiggleArpeggiatoUp"
