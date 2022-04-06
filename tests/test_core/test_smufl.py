import pytest

from neoscore.core import smufl

"""  glyphnames.json
"6stringTabClef": {
        "codepoint": "\uE06D",
        "description": "6-string tab clef"
    }
"""


def test_get_basic_glyph_info():
    assert smufl.get_basic_glyph_info("6stringTabClef") == {
        "codepoint": "\uE06D",
        "description": "6-string tab clef",
    }
    with pytest.raises(KeyError) as err:
        smufl.get_basic_glyph_info("clef")
    assert (
        'Could not find glyph name "clef". '
        + "Maybe you meant one of these? clef8 / cClef / clef15 / gClef / fClef"
        in str(err.value)
    )


def test_char_from_glyph_name():
    assert smufl.char_from_glyph_name("6stringTabClef") == "\uE06D"
    with pytest.raises(KeyError):
        smufl.char_from_glyph_name("clef")


def test_description_from_glyph_name():
    assert smufl.description_from_glyph_name("6stringTabClef") == "6-string tab clef"
    with pytest.raises(KeyError):
        smufl.description_from_glyph_name("nonexistent name")


"""  ranges.json
    "accordion": {
        "description": "Accordion",
        "glyphs": [
            "accdnRH3RanksPiccolo",
"""


def test_glyph_range_key():
    assert smufl.get_glyph_range_key("accdnRH3RanksPiccolo") == "accordion"
    with pytest.raises(KeyError):
        smufl.get_glyph_range_key("nonexistent name")


def test_get_glyph_classes():
    expected_match = {
        "accidentals",
        "accidentalsSagittalMixed",
        "accidentalsStandard",
        "combiningStaffPositions",
    }
    result_match = smufl.get_glyph_classes("accidentalFlat")
    assert result_match == expected_match
