import unittest

from neoscore.core import neoscore
from neoscore.utils.units import Mm
from neoscore.western.brace import Brace
from neoscore.western.staff import Staff


class TestBrace(unittest.TestCase):
    def setUp(self):
        neoscore.setup()

    def test_scaling_alternate_glyphs(self):
        top_staff = Staff((Mm(0), Mm(0)), None, length=Mm(100))
        bottom_staff = Staff((Mm(0), Mm(20)), None, length=Mm(100))
        small_brace = Brace(Mm(0), {top_staff})
        assert small_brace.music_chars[0].canonical_name == "braceSmall"
        large_brace = Brace(Mm(0), {top_staff, bottom_staff})
        assert large_brace.music_chars[0].canonical_name == "braceLarge"
