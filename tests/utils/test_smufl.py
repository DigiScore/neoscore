import pytest

from brown.utils import smufl

"""

"6stringTabClef": {
        "codepoint": "\uE06D",
        "description": "6-string tab clef"
    }

"""


def test_look_up_glyph_name():
    assert(smufl.look_up_glyph_name("6stringTabClef") ==
           {"codepoint": "\uE06D",
            "description": "6-string tab clef"})
    with pytest.raises(KeyError):
        smufl.look_up_glyph_name("nonexistent name")


def test_char_from_glyph_name():
    assert(smufl.char_from_glyph_name("6stringTabClef") == "\uE06D")
    with pytest.raises(KeyError):
        smufl.char_from_glyph_name("nonexistent name")


def test_description_from_glyph_name():
    assert(smufl.description_from_glyph_name("6stringTabClef") == "6-string tab clef")
    with pytest.raises(KeyError):
        smufl.description_from_glyph_name("nonexistent name")
