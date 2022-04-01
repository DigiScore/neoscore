from neoscore.core.music_font import MusicFont
from neoscore.utils.units import Mm, Unit

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
