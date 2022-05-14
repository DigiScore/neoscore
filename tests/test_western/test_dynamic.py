import pytest

from neoscore.core.units import Mm
from neoscore.western.dynamic import Dynamic, DynamicStringError
from neoscore.western.staff import Staff

from ..helpers import AppTest


class TestDynamic(AppTest):
    def setUp(self):
        super().setUp()
        self.staff = Staff((Mm(0), Mm(0)), parent=None, length=Mm(100))

    def test_parse_dynamic_string(self):
        self.assertEqual(
            Dynamic._parse_dynamic_string("pmfrszn"),
            [
                "dynamicPiano",
                "dynamicMezzo",
                "dynamicForte",
                "dynamicRinforzando",
                "dynamicSforzando",
                "dynamicZ",
                "dynamicNiente",
            ],
        )

    def test_parsing_invalid_string_raises_exception(self):
        with pytest.raises(DynamicStringError):
            Dynamic._parse_dynamic_string("h")

    def test_ppp(self):
        self.assertEqual(
            Dynamic.ppp((Mm(0), Mm(0)), self.staff).text,
            Dynamic((Mm(0), Mm(0)), self.staff, "ppp").text,
        )

    def test_pp(self):
        self.assertEqual(
            Dynamic.pp((Mm(0), Mm(0)), self.staff).text,
            Dynamic((Mm(0), Mm(0)), self.staff, "pp").text,
        )

    def test_p(self):
        self.assertEqual(
            Dynamic.p((Mm(0), Mm(0)), self.staff).text,
            Dynamic((Mm(0), Mm(0)), self.staff, "p").text,
        )

    def test_mp(self):
        self.assertEqual(
            Dynamic.mp((Mm(0), Mm(0)), self.staff).text,
            Dynamic((Mm(0), Mm(0)), self.staff, "mp").text,
        )

    def test_mf(self):
        self.assertEqual(
            Dynamic.mf((Mm(0), Mm(0)), self.staff).text,
            Dynamic((Mm(0), Mm(0)), self.staff, "mf").text,
        )

    def test_f(self):
        self.assertEqual(
            Dynamic.f((Mm(0), Mm(0)), self.staff).text,
            Dynamic((Mm(0), Mm(0)), self.staff, "f").text,
        )

    def test_ff(self):
        self.assertEqual(
            Dynamic.ff((Mm(0), Mm(0)), self.staff).text,
            Dynamic((Mm(0), Mm(0)), self.staff, "ff").text,
        )

    def test_fff(self):
        self.assertEqual(
            Dynamic.fff((Mm(0), Mm(0)), self.staff).text,
            Dynamic((Mm(0), Mm(0)), self.staff, "fff").text,
        )

    def test_sfz(self):
        self.assertEqual(
            Dynamic.sfz((Mm(0), Mm(0)), self.staff).text,
            Dynamic((Mm(0), Mm(0)), self.staff, "sfz").text,
        )

    def test_fp(self):
        self.assertEqual(
            Dynamic.fp((Mm(0), Mm(0)), self.staff).text,
            Dynamic((Mm(0), Mm(0)), self.staff, "fp").text,
        )
