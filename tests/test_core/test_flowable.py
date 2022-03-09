import unittest

import pytest

from brown.core import brown
from brown.core.flowable import Flowable, OutOfBoundsError
from brown.core.paper import Paper
from brown.utils.point import Point
from brown.utils.units import Mm


class TestFlowable(unittest.TestCase):
    def setUp(self):
        brown.setup(Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        # live_width == Mm(160)
        # live_height == Mm(257)

    def test_init(self):
        test_flowable = Flowable((Mm(10), Mm(11)), Mm(1000), Mm(100), Mm(5))
        assert test_flowable.pos == Point(Mm(10), Mm(11))
        assert test_flowable.x == Mm(10)
        assert test_flowable.y == Mm(11)
        assert test_flowable.length == Mm(1000)
        assert test_flowable.height == Mm(100)
        assert test_flowable.y_padding == Mm(5)

    def test_self_pos_manipulation(self):
        test_flowable = Flowable((Mm(10), Mm(11)), Mm(1000), Mm(100), Mm(5))
        test_flowable.x = Mm(20)
        assert test_flowable.pos.x == Mm(20)
        test_flowable.y = Mm(21)
        assert test_flowable.pos.y == Mm(21)

    def test_generate_layout_controllers_with_only_one_line(self):
        test_flowable = Flowable((Mm(9), Mm(11)), Mm(100), Mm(50), Mm(5))
        test_flowable._generate_layout_controllers()
        assert len(test_flowable.layout_controllers) == 1
        assert test_flowable.layout_controllers[0].flowable_x == Mm(0)
        assert test_flowable.layout_controllers[0].pos == Point(Mm(9), Mm(11))
        assert test_flowable.layout_controllers[0].page == brown.document.pages[0]

    def test_generate_layout_controllers_with_two_lines(self):
        live_width = brown.document.paper.live_width
        test_flowable = Flowable((Mm(0), Mm(0)), live_width * 1.5, Mm(50), Mm(5))
        # Should result in 2 lines separated by 1 line break
        test_flowable._generate_layout_controllers()
        assert len(test_flowable.layout_controllers) == 2
        assert test_flowable.layout_controllers[1].flowable_x == live_width
        assert test_flowable.layout_controllers[1].page == brown.document.pages[0]

    def test_generate_layout_controllers_with_many_lines(self):
        live_width = brown.document.paper.live_width
        test_flowable = Flowable((Mm(0), Mm(0)), live_width * 3.5, Mm(50), Mm(5))
        # Should result in four lines separated by 3 line breaks
        test_flowable._generate_layout_controllers()
        assert len(test_flowable.layout_controllers) == 4
        assert test_flowable.layout_controllers[1].flowable_x == live_width
        assert test_flowable.layout_controllers[2].flowable_x == live_width * 2
        assert test_flowable.layout_controllers[3].flowable_x == live_width * 3

    def test_generate_layout_controllers_with_two_pages(self):
        live_width = brown.document.paper.live_width
        test_flowable = Flowable((Mm(0), Mm(0)), live_width * 1.5, Mm(256), Mm(5))
        # Should result in two lines separated by one page break
        test_flowable._generate_layout_controllers()
        assert len(test_flowable.layout_controllers) == 2
        assert test_flowable.layout_controllers[1].flowable_x == live_width

    def test_generate_layout_controllers_with_many_pages(self):
        live_width = brown.document.paper.live_width
        test_flowable = Flowable((Mm(0), Mm(0)), live_width * 3.5, Mm(256), Mm(5))
        test_flowable._generate_layout_controllers()
        assert len(test_flowable.layout_controllers) == 4
        assert test_flowable.layout_controllers[1].flowable_x == live_width
        assert test_flowable.layout_controllers[2].flowable_x == live_width * 2
        assert test_flowable.layout_controllers[3].flowable_x == live_width * 3

    def test_generate_layout_controllers_new_lines_have_padding(self):
        live_width = brown.document.paper.live_width
        test_flowable = Flowable((Mm(0), Mm(0)), live_width * 3.5, Mm(1000), Mm(5))
        test_flowable._generate_layout_controllers()
        # Test that every NewLine which is not also a page break has the expected
        # y_padding from the flowable
        current_page = None
        for line in test_flowable.layout_controllers:
            if current_page != line.page:
                current_page = line.page
                continue
            assert line.margin_bottom == test_flowable.y_padding

    def test_generate_layout_controllers_on_new_pages_have_no_padding(self):
        live_width = brown.document.paper.live_width
        test_flowable = Flowable((Mm(0), Mm(0)), live_width * 3.5, Mm(1000), Mm(5))
        test_flowable._generate_layout_controllers()
        # Test that every NewLine which is also a page break
        # has no y_padding (is aligned with the top of the live page area)
        current_page = None
        for line in test_flowable.layout_controllers:
            if current_page == line.page:
                continue
            current_page = line.page
            assert line.margin_bottom == Mm(0)

    # For reference
    # page live width == Mm(160)
    # page live height == Mm(257)

    def test_x_pos_rel_to_line_start(self):
        test_flowable = Flowable((Mm(10), Mm(0)), Mm(500), Mm(90), Mm(5))
        assert test_flowable.dist_to_line_start(Mm(170)) == Mm(20)
        assert test_flowable.dist_to_line_start(Mm(320)) == Mm(10)

    def testdist_to_line_end(self):
        test_flowable = Flowable((Mm(10), Mm(0)), Mm(500), Mm(90), Mm(5))
        assert test_flowable.dist_to_line_end(Mm(170)) == Mm(-140)
        assert test_flowable.dist_to_line_end(Mm(320)) == Mm(-150)

    def testlast_break_at(self):
        test_flowable = Flowable((Mm(10), Mm(0)), Mm(500), Mm(90), Mm(5))
        assert (
            test_flowable.last_break_at(Mm(140)) == test_flowable.layout_controllers[0]
        )
        assert (
            test_flowable.last_break_at(Mm(180)) == test_flowable.layout_controllers[1]
        )

    def testlast_break_at_raises_out_of_bounds_when_needed(self):
        test_flowable = Flowable((Mm(10), Mm(0)), Mm(10000), Mm(90), Mm(5))
        with pytest.raises(OutOfBoundsError):
            test_flowable.last_break_at(Mm(10000000))
