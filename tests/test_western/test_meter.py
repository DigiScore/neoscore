import unittest

from neoscore.western.meter import COMMON_TIME, CUT_TIME, Meter


class TestMeter(unittest.TestCase):
    def test_explicit_init(self):
        meter = Meter(["foo"], ["bar", "biz"])
        assert meter.upper_text_glyph_names == ["foo"]
        assert meter.lower_text_glyph_names == ["bar", "biz"]

    def test_common_time(self):
        assert COMMON_TIME.upper_text_glyph_names == ["timeSigCommon"]
        assert COMMON_TIME.lower_text_glyph_names == []

    def test_cut_time(self):
        assert CUT_TIME.upper_text_glyph_names == ["timeSigCutCommon"]
        assert CUT_TIME.lower_text_glyph_names == []

    def test_numeric_constructor_with_single_upper_number(self):
        assert Meter.numeric(3, 8) == Meter(["timeSig3"], ["timeSig8"])
        assert Meter.numeric(12, 4) == Meter(["timeSig1", "timeSig2"], ["timeSig4"])
        assert Meter.numeric(4, 16) == Meter(["timeSig4"], ["timeSig1", "timeSig6"])

    def test_numeric_constructor_with_list_of_upper_numbers(self):
        assert Meter.numeric([3, 5], 8) == Meter(
            ["timeSig3", "timeSigPlus", "timeSig5"], ["timeSig8"]
        )
        assert Meter.numeric([3, 5, 10], 16) == Meter(
            [
                "timeSig3",
                "timeSigPlus",
                "timeSig5",
                "timeSigPlus",
                "timeSig1",
                "timeSig0",
            ],
            ["timeSig1", "timeSig6"],
        )
        # list of single int should behave like plain int
        assert Meter.numeric([4], 4) == Meter.numeric(4, 4)

    def test_from_def(self):
        assert Meter.from_def(Meter.numeric(4, 4)) == Meter.numeric(4, 4)
        assert Meter.from_def((4, 4)) == Meter.numeric(4, 4)
        assert Meter.from_def(([4, 2], 4)) == Meter.numeric([4, 2], 4)
