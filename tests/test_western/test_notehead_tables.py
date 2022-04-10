from dataclasses import asdict

from neoscore.core.music_font import MusicFont
from neoscore.core.units import Mm
from neoscore.western import notehead_tables
from tests.helpers import AppTest


class TestNoteheadTables(AppTest):
    def test_all_glyphs_in_all_tables_exist(self):
        font = MusicFont("Bravura", Mm)
        for table in notehead_tables.ALL_TABLES:
            if all((val == "" for val in asdict(table).values())):
                # This is the INVISIBLE table, which is expected to fail this check
                continue
            font.glyph_info(table.double_whole, None)
            font.glyph_info(table.whole, None)
            font.glyph_info(table.half, None)
            font.glyph_info(table.short, None)
