import unittest
import pytest
from neoscore.core import neoscore
from neoscore.core.music_font import MusicFont
from neoscore.utils.units import Mm, Unit
from neoscore.utils import smufl
from neoscore.models.glyph_info import GlyphInfo
from neoscore.utils.exceptions import MusicFontGlyphNotFoundError

from ..helpers import AppTest


class EquivalentUnit(Unit):
    pass


class TestMusicFont(AppTest):
    def test_modified(self):
        font = MusicFont("Bravura", Unit)
        # Since only Bravura is currently provided, we can't really
        # test different families used in `modified`, but we can at
        # least run this branch on the same family.
        modifying_family_name = font.modified(family_name="Bravura")
        assert modifying_family_name.family_name == "Bravura"
        assert modifying_family_name.unit == Unit
        modifying_unit = font.modified(unit=Mm)
        assert modifying_unit.family_name == "Bravura"
        assert modifying_unit.unit == Mm

    def test__eq__(self):
        font = MusicFont("Bravura", Unit)
        assert font == MusicFont("Bravura", Unit)
        assert font == MusicFont("Bravura", EquivalentUnit)
        # (Can't test case of different family name since only Bravura exists)
        # assert font != MusicFont("Foo", Unit)
        assert font != MusicFont("Bravura", Mm)

    def test__hash__(self):
        font = MusicFont("Bravura", Unit)
        assert hash(font) == hash(MusicFont("Bravura", Unit))
        assert hash(font) == hash(MusicFont("Bravura", EquivalentUnit))
        # (Can't test case of different family name since only Bravura exists)
        # assert hash(font) != MusicFont("Foo", Unit)
        assert hash(font) != hash(MusicFont("Bravura", Mm))

    def test_glyph_info_for_all_required_glyphs(self):
        font = MusicFont("Bravura", Unit)
        # test each glyph in the glyphnamelist json
        for testGlyph in smufl.glyph_names:
            test = font.glyph_info(testGlyph).canonical_name
            raw = font._glyph_info(testGlyph).canonical_name
            # assert test == testGlyph
            assert test == raw

    def test_glyph_info_for_one_alternate_glyph(self):
        font = MusicFont("Bravura", Unit)
        testGlyph = font.glyph_info('brace', 1)
        assert testGlyph.canonical_name == 'braceSmall'
        assert testGlyph.codepoint == "\uF400"

    def test_glyph_info_for_last_alternate_glyph(self):
        font = MusicFont("Bravura", Unit)
        testGlyph = font.glyph_info('brace', 4)
        assert testGlyph.canonical_name == 'braceFlat'
        assert testGlyph.codepoint == "\uF403"

    def test_glyph_info_for_Foo_glyph(self):
        font = MusicFont("Bravura", Unit)
        with pytest.raises(MusicFontGlyphNotFoundError):
            font.glyph_info('Foo')

    def test_glyph_info_for_out_of_range_alternative_glyph(self):
        font = MusicFont("Bravura", Unit)
        with pytest.raises(MusicFontGlyphNotFoundError):
            font.glyph_info('brace', 6)