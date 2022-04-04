import pytest

from neoscore.core.music_font import MusicFont
from neoscore.utils import smufl
from neoscore.utils.exceptions import MusicFontGlyphNotFoundError
from neoscore.utils.rect import Rect
from neoscore.utils.units import Mm, Unit, convert_all_to_unit

from ..helpers import AppTest


class EquivalentUnit(Unit):
    pass


class TestMusicFont(AppTest):
    def setUp(self):
        super().setUp()
        self.font = MusicFont("Bravura", Unit)

    def test_modified(self):
        # Since only Bravura is currently provided, we can't really
        # test different families used in `modified`, but we can at
        # least run this branch on the same family.
        modifying_family_name = self.font.modified(family_name="Bravura")
        assert modifying_family_name.family_name == "Bravura"
        assert modifying_family_name.unit == Unit
        modifying_unit = self.font.modified(unit=Mm)
        assert modifying_unit.family_name == "Bravura"
        assert modifying_unit.unit == Mm

    def test__eq__(self):
        assert self.font == MusicFont("Bravura", Unit)
        assert self.font == MusicFont("Bravura", EquivalentUnit)
        # (Can't test case of different family name since only Bravura exists)
        # assert font != MusicFont("Foo", Unit)
        assert self.font != MusicFont("Bravura", Mm)

    def test__hash__(self):
        assert hash(self.font) == hash(MusicFont("Bravura", Unit))
        assert hash(self.font) == hash(MusicFont("Bravura", EquivalentUnit))
        # (Can't test case of different family name since only Bravura exists)
        # assert hash(font) != MusicFont("Foo", Unit)
        assert hash(self.font) != hash(MusicFont("Bravura", Mm))

    def test_every_glyphname_in_smufl(self):
        for g in smufl.glyph_names:
            testGlyph = self.font.glyph_info(g)
            assert g == testGlyph.canonical_name

    def test_complete_info_for_normal_glyph_with_anchors(self):
        test_glyph = self.font.glyph_info("accidental3CommaSharp")
        assert test_glyph.canonical_name == "accidental3CommaSharp"
        assert test_glyph.codepoint == "\ue452"
        assert test_glyph.description == "3-comma sharp"
        assert test_glyph.bounding_rect == Rect(
            x=Unit(0), y=Unit(-2.044), width=Unit(1.828), height=Unit(3.436)
        )
        assert test_glyph.advance_width == Unit(1.736)
        assert test_glyph.anchors == {
            "cutOutNW": [0.888, 1.516],
            "cutOutSE": [1.108, 0.856],
            "cutOutSW": [0.108, -0.956],
        }

    def test_optional_glyph_info(self):
        test_glyph_no_description = self.font._check_optional_glyphs(
            "accidentalDoubleFlatParens"
        )
        assert test_glyph_no_description[0] == "\uF5E4"
        assert test_glyph_no_description[1] == None
        test_glyph_with_description = self.font._check_optional_glyphs(
            "4stringTabClefSerif"
        )
        assert test_glyph_with_description[0] == "\uF40D"
        assert test_glyph_with_description[1] == "4-string tab clef (serif)"

    def test_glyph_info_for_one_alternate_glyph(self):
        test_glyph = self.font.glyph_info("brace", 1)
        assert test_glyph.canonical_name == "braceSmall"
        assert test_glyph.codepoint == "\uF400"

    def test_glyph_info_for_last_alternate_glyph(self):
        test_glyph = self.font.glyph_info("brace", 4)
        assert test_glyph.canonical_name == "braceFlat"
        assert test_glyph.codepoint == "\uF403"

    def test_glyph_info_for_foo_glyph(self):
        with pytest.raises(MusicFontGlyphNotFoundError):
            self.font.glyph_info("Foo")

    def test_glyph_info_for_out_of_range_alternative_glyph(self):
        with pytest.raises(MusicFontGlyphNotFoundError):
            self.font.glyph_info("brace", 6)

    def test_bbox_translations_on_foo_boundrys(self):
        rnd_dict = {"bBoxNE": [-10, 10], "bBoxSW": [10, -10]}
        convert_all_to_unit(rnd_dict, self.font.unit)
        rect_result = self.font._convert_bbox_to_rect(rnd_dict)

        assert rect_result == Rect(
            x=Unit(10), y=Unit(-10.0), width=Unit(-20.0), height=Unit(20.0)
        )
