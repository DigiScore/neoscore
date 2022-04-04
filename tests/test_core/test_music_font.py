import unittest
import pytest
from random import uniform
from neoscore.core import neoscore
from neoscore.core.music_font import MusicFont
from neoscore.utils.units import Mm, Unit
from neoscore.utils import smufl
from neoscore.utils.rect import Rect
from neoscore.utils.units import Unit, convert_all_to_unit
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

    def test_every_glyphname_in_smufl(self):
        font = MusicFont("Bravura", Unit)
        for g in smufl.glyph_names:
            testGlyph = font.glyph_info(g)
            assert g == testGlyph.canonical_name

    def test_complete_info_for_normal_glyph_with_anchors(self):
        font = MusicFont("Bravura", Unit)
        test_glyph = font.glyph_info('accidental3CommaSharp')
        assert test_glyph.canonical_name == 'accidental3CommaSharp'
        assert test_glyph.codepoint == "\ue452"
        assert test_glyph.description == "3-comma sharp"
        assert test_glyph.bounding_box == Rect(x=Unit(0),
                                              y=Unit(-2.044),
                                              width=Unit(1.828),
                                              height=Unit(3.436)
                                              )
        assert test_glyph.advance_width == Unit(1.736)
        assert test_glyph.anchors == {'cutOutNW': [0.888, 1.516],
                                     'cutOutSE': [1.108, 0.856],
                                     'cutOutSW': [0.108, -0.956]
                                     }

    def test_glyph_info_for_one_alternate_glyph(self):
        font = MusicFont("Bravura", Unit)
        test_glyph = font.glyph_info('brace', 1)
        assert test_glyph.canonical_name == 'braceSmall'
        assert test_glyph.codepoint == "\uF400"

    def test_glyph_info_for_last_alternate_glyph(self):
        font = MusicFont("Bravura", Unit)
        test_glyph = font.glyph_info('brace', 4)
        assert test_glyph.canonical_name == 'braceFlat'
        assert test_glyph.codepoint == "\uF403"

    def test_glyph_info_for_foo_glyph(self):
        font = MusicFont("Bravura", Unit)
        with pytest.raises(MusicFontGlyphNotFoundError):
            font.glyph_info('Foo')

    def test_glyph_info_for_out_of_range_alternative_glyph(self):
        font = MusicFont("Bravura", Unit)
        with pytest.raises(MusicFontGlyphNotFoundError):
            font.glyph_info('brace', 6)

    def test_all_smufl_bbox_translations_to_rect(self):
        font = MusicFont("Bravura", Unit)
        b_box_dict = font.metadata["glyphBBoxes"].items()
        for glyph, box in b_box_dict:
            convert_all_to_unit(box, font.unit)
            rect = Rect(x=box["bBoxSW"][0],
                        y=box["bBoxNE"][1] * -1,
                        width=box["bBoxNE"][0] - box["bBoxSW"][0],
                        height=box["bBoxNE"][1] - box["bBoxSW"][1]
                        )
            assert font._convert_bbox_to_rect(box) == rect

    def test_bbox_translations_on_random_foo(self):
        font = MusicFont("Bravura", Unit)
        for test in range (20):
            rnd_dict = {"bBoxNE": [font.unit(uniform(-10.0, 10.0)),
                                   font.unit(uniform(-10.0, 10.0))],
                        "bBoxSW": [font.unit(uniform(-10.0, 10.0)),
                                   font.unit(uniform(-10.0, 10.0))]
                        }
            # convert_all_to_unit(rnd_dict, font.unit)
            rect = Rect(x=rnd_dict["bBoxSW"][0],
                        y=rnd_dict["bBoxNE"][1] * -1,
                        width=rnd_dict["bBoxNE"][0] - rnd_dict["bBoxSW"][0],
                        height=rnd_dict["bBoxNE"][1] - rnd_dict["bBoxSW"][1]
                        )
            assert font._convert_bbox_to_rect(rnd_dict) == rect


