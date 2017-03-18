import unittest

from brown.core import brown
from brown.core.staff import Staff
from brown.core.brace import Brace
from brown.utils.units import Mm


class TestBrace(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_scaling_alternate_glyphs(self):
        top_staff = Staff((Mm(0), Mm(0)), Mm(100), frame=None)
        bottom_staff = Staff((Mm(0), Mm(20)), Mm(100), frame=None)
        small_brace = Brace(Mm(0), Mm(10), {top_staff})
        assert(small_brace.music_chars[0].canonical_name == 'braceSmall')
        large_brace = Brace(Mm(0), Mm(10), {top_staff, bottom_staff})
        assert(large_brace.music_chars[0].canonical_name == 'braceLarge')
