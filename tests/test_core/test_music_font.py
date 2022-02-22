import unittest

import pytest

from brown.core import brown
from brown.core.music_font import MusicFont
from brown.utils.exceptions import MusicFontMetadataNotFoundError
from brown.utils.units import Mm, Unit


class TestMusicFont(unittest.TestCase):
    def setUp(self):
        brown.setup()

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
