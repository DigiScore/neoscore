import unittest

from nose.tools import assert_raises

from brown.core import brown
from brown.primitives.dynamic import Dynamic, DynamicStringError
from brown.primitives.staff import Staff
from brown.utils.units import Mm


class TestNotehead(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.staff = Staff((Mm(0), Mm(0)), Mm(100), frame=None)

    def test_parse_dynamic_string(self):
        self.assertEqual(Dynamic._parse_dynamic_string('pmfrszn'),
                         ['dynamicPiano',
                          'dynamicMezzo',
                          'dynamicForte',
                          'dynamicRinforzando',
                          'dynamicSforzando',
                          'dynamicZ',
                          'dynamicNiente'])

    def test_parsing_invalid_string_raises_exception(self):
        with assert_raises(DynamicStringError):
            Dynamic._parse_dynamic_string('h')

    def test_ppp(self):
        self.assertEqual(Dynamic.ppp((Mm(0), Mm(0)), self.staff).text,
                         Dynamic((Mm(0), Mm(0)), 'ppp', self.staff).text)

    def test_pp(self):
        self.assertEqual(Dynamic.pp((Mm(0), Mm(0)), self.staff).text,
                         Dynamic((Mm(0), Mm(0)), 'pp', self.staff).text)

    def test_p(self):
        self.assertEqual(Dynamic.p((Mm(0), Mm(0)), self.staff).text,
                         Dynamic((Mm(0), Mm(0)), 'p', self.staff).text)

    def test_mp(self):
        self.assertEqual(Dynamic.mp((Mm(0), Mm(0)), self.staff).text,
                         Dynamic((Mm(0), Mm(0)), 'mp', self.staff).text)

    def test_mf(self):
        self.assertEqual(Dynamic.mf((Mm(0), Mm(0)), self.staff).text,
                         Dynamic((Mm(0), Mm(0)), 'mf', self.staff).text)

    def test_f(self):
        self.assertEqual(Dynamic.f((Mm(0), Mm(0)), self.staff).text,
                         Dynamic((Mm(0), Mm(0)), 'f', self.staff).text)

    def test_ff(self):
        self.assertEqual(Dynamic.ff((Mm(0), Mm(0)), self.staff).text,
                         Dynamic((Mm(0), Mm(0)), 'ff', self.staff).text)

    def test_fff(self):
        self.assertEqual(Dynamic.fff((Mm(0), Mm(0)), self.staff).text,
                         Dynamic((Mm(0), Mm(0)), 'fff', self.staff).text)

    def test_sfz(self):
        self.assertEqual(Dynamic.sfz((Mm(0), Mm(0)), self.staff).text,
                         Dynamic((Mm(0), Mm(0)), 'sfz', self.staff).text)

    def test_fp(self):
        self.assertEqual(Dynamic.fp((Mm(0), Mm(0)), self.staff).text,
                         Dynamic((Mm(0), Mm(0)), 'fp', self.staff).text)
