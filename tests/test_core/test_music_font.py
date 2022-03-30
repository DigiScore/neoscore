import unittest

from neoscore.core import neoscore
from neoscore.core.music_font import MusicFont
from neoscore.utils.units import Mm, Unit
from neoscore.utils import smufl

class EquivalentUnit(Unit):
    pass


class TestMusicFont(unittest.TestCase):
    def setUp(self):
        neoscore.setup()

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

    def test_every_SMuFL_glyph(self):
        font = MusicFont("Bravura", Unit)
        # test each glyph in the glyphnamelist json
        for testGlyph in smufl.glyph_names:
            assert





        if full_test:
            glyphCount = 0



                # test for every alt option between 1 - 3
                for alt in range(10):
                    if alt == 0:
                        alt = None
                    elif alt == 9:
                        testGlyph = 'garbage'
                    # print(f'\n\t\t\t\t{testGlyph}, {alt}, {glyphCount}')
                    try:
                        test_info_dict = font._glyph_info(testGlyph, alt)
                        print(f'returned dict = {test_info_dict}')
                    except Exception as e:
                        print(f'error for {testGlyph, alt, e}')

                    # if returns filled dict AND not an alterante glyph add to count
                    if len(test_info_dict) > 0 and alt == None:
                        glyphCount += 1

            # tally up - should be the same value
            print(f'total glyph count === {glyphCount}')
            print(f'total glyph list name count === {len(smufl.glyph_names)}')

        else:
            oneTestGlyph = ["accidentalDoubleFlatParens",
                            '4stringTabClef',
                            'noteFaHalf',
                            '4stringTabClefSerif',
                            'gClef4Above']
            for test in oneTestGlyph:
                r = font._glyph_info(test)
                print(f'\nreturn dict == === == {r}')
