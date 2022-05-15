import pytest

from neoscore.core import smufl
from neoscore.core.exceptions import MusicFontGlyphNotFoundError
from neoscore.core.music_font import MusicFont
from neoscore.core.point import Point
from neoscore.core.rect import Rect
from neoscore.core.units import Mm, Unit, convert_all_to_unit

from ..helpers import AppTest


class EquivalentUnit(Unit):
    pass


class TestMusicFont(AppTest):
    def setUp(self):
        super().setUp()
        self.font = MusicFont("Bravura", Unit)

    def test_init_with_unit_type(self):
        font = MusicFont("Bravura", Mm)
        self.assertAlmostEqual(font.unit.CONVERSION_RATE, 2.8346456664)

    def test_init_with_unit_value(self):
        font = MusicFont("Bravura", Mm(2))
        self.assertAlmostEqual(font.unit.CONVERSION_RATE, 5.6692913328)

    def test_modified(self):
        # Since only Bravura is currently provided, we can't really
        # test different families used in ``modified``, but we can at
        # least run this branch on the same family.
        modifying_family_name = self.font.modified(family_name="Bravura")
        assert modifying_family_name.family_name == "Bravura"
        assert modifying_family_name.unit == Unit
        modifying_unit = self.font.modified(unit=Mm)
        assert modifying_unit.family_name == "Bravura"
        assert modifying_unit.unit == Mm

    def test__str__(self):
        font = MusicFont("Bravura", Unit)
        assert str(font) == "MusicFont('Bravura', <unit(1) = Mm(0.353)>)"

    def test_every_glyphname_in_smufl(self):
        for g in smufl.glyph_names:
            test_glyph = self.font.glyph_info(g)
            assert g == test_glyph.canonical_name

    def test_complete_info_for_normal_glyph_with_anchors(self):
        test_glyph = self.font.glyph_info("accidental3CommaSharp")
        assert test_glyph.canonical_name == "accidental3CommaSharp"
        assert test_glyph.codepoint == "\ue452"
        assert test_glyph.description == "3-comma sharp"
        assert test_glyph.bounding_rect == Rect(
            Unit(0), Unit(-2.044), Unit(1.828), Unit(3.436)
        )
        assert test_glyph.advance_width == Unit(1.736)
        assert test_glyph.anchors == {
            "cutOutNW": Point(self.font.unit(0.888), self.font.unit(-1.516)),
            "cutOutSE": Point(self.font.unit(1.108), self.font.unit(-0.856)),
            "cutOutSW": Point(self.font.unit(0.108), self.font.unit(0.956)),
        }

    def test_optional_glyph_info(self):
        test_glyph_no_description = self.font._check_optional_glyphs(
            "accidentalDoubleFlatParens"
        )
        assert test_glyph_no_description[0] == "\uF5E4"
        assert test_glyph_no_description[1] is None
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
        smufl_bbox = {"bBoxNE": [-10, 10], "bBoxSW": [10, -10]}
        convert_all_to_unit(smufl_bbox, self.font.unit)
        rect_result = self.font._convert_bbox_to_rect(smufl_bbox)
        assert rect_result == Rect(Unit(10), Unit(-10.0), Unit(-20.0), Unit(20.0))

    def test_glyph_anchors_converted_to_neoscore_points(self):
        assert self.font.metadata["glyphsWithAnchors"]["accidentalSharp"] == {
            "cutOutNE": [0.84, 0.896],
            "cutOutNW": [0.144, 0.568],
            "cutOutSE": [0.84, -0.596],
            "cutOutSW": [0.144, -0.896],
        }
        assert self.font._load_glyph_anchors("accidentalSharp") == {
            "cutOutNE": Point(Unit(0.84), Unit(-0.896)),
            "cutOutNW": Point(Unit(0.144), Unit(-0.568)),
            "cutOutSE": Point(Unit(0.84), Unit(0.596)),
            "cutOutSW": Point(Unit(0.144), Unit(0.896)),
        }
