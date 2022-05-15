import pytest

from neoscore.core.exceptions import NoAncestorWithMusicFontError
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.music_text import MusicText
from neoscore.core.point import ORIGIN
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import Inch, Mm

from ..helpers import AppTest


class TestMusicPath(AppTest):
    def setUp(self):
        super().setUp()
        self.font = MusicFont("Bravura", Mm)

    def test_init_with_ancestor_with_font(self):
        parent_1 = MusicText(ORIGIN, None, "accidentalSharp", self.font)
        parent_2 = PositionedObject(ORIGIN, parent_1)
        mp = MusicPath(ORIGIN, parent_2)
        assert mp.music_font == self.font

    def test_init_with_explicit_font_and_no_ancestor_font(self):
        mp = MusicPath(ORIGIN, None, font=self.font)
        assert mp.music_font == self.font

    def test_init_with_explicit_font_overrides_ancestor_font(self):
        parent_1 = MusicText(ORIGIN, None, "accidentalSharp", self.font)
        parent_2 = PositionedObject(ORIGIN, parent_1)
        other_font = MusicFont("Bravura", Inch)
        mp = MusicPath(ORIGIN, parent_2, font=other_font)
        assert mp.music_font == other_font

    def test_init_with_no_font_fails(self):
        parent = PositionedObject(ORIGIN, None)
        with pytest.raises(NoAncestorWithMusicFontError):
            MusicPath(ORIGIN, parent)
