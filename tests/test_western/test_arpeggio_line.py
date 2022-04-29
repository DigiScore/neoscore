from neoscore.core.brush import Brush
from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import Pen
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import Mm
from neoscore.western.arpeggio_line import ArpeggioLine
from tests.helpers import AppTest


class TestRepeatingMusicTextLine(AppTest):
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
        assert len(arp.music_chars) == 14
        assert arp.music_chars[0] == MusicChar(font, "wiggleArpeggiatoUp")
        assert arp.music_chars[-1] == MusicChar(font, "wiggleArpeggiatoUpArrow")
        assert arp.brush == Brush("#ff0000")
        assert arp.pen == Pen("#00ff00")
        assert arp.background_brush == Brush("#0000ff")
