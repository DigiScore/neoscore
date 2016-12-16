from nose.tools import assert_raises
import unittest

from brown.core.paper import Paper
from brown.core import brown
from brown.utils.units import Mm
from brown.utils.point import Point
from brown.core.flowable_frame import FlowableFrame, OutOfBoundsError
from brown.core.auto_new_line import AutoNewLine
from brown.core.auto_new_page import AutoNewPage


# TODO: These tests could use some more cleanups...


class TestFlowableFrame(unittest.TestCase):

    def setUp(self):
        brown.setup(
            Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        # live_width == Mm(160)
        # live_height == Mm(257)

    def test_init(self):
        test_frame = FlowableFrame((Mm(10), Mm(11)), Mm(1000), Mm(100), Mm(5))
        assert(test_frame.x == Mm(10))
        assert(test_frame.y == Mm(11))
        assert(test_frame.pos.x == Mm(10))
        assert(test_frame.pos.y == Mm(11))
        assert(test_frame.width == Mm(1000))
        assert(test_frame.height == Mm(100))
        assert(test_frame.y_padding == Mm(5))

    def test_self_pos_manipulation(self):
        test_frame = FlowableFrame((Mm(10), Mm(11)), Mm(1000), Mm(100), Mm(5))
        test_frame.x = Mm(20)
        assert(test_frame.pos.x == Mm(20))
        assert(test_frame.x == Mm(20))
        test_frame.y = Mm(21)
        assert(test_frame.pos.y == Mm(21))
        assert(test_frame.y == Mm(21))

    # Layout generation tests #################################################

    def test_generate_layout_controllers_with_only_one_line(self):
        test_frame = FlowableFrame((Mm(9), Mm(11)), Mm(100), Mm(50), Mm(5))
        test_frame._generate_layout_controllers()
        assert(len(test_frame.layout_controllers) == 1)
        assert(test_frame.layout_controllers[0].flowable_frame == test_frame)
        assert(test_frame.layout_controllers[0].x == Mm(0))
        assert(test_frame.layout_controllers[0].page_pos == Point(Mm(9), Mm(11)))

    # BELOW ARE BROKEN

    def test_generate_layout_controllers_with_two_lines(self):
        live_width = brown.document.paper.live_width
        test_frame = FlowableFrame((Mm(0), Mm(0)), live_width * 1.5, Mm(50), Mm(5))
        # Should result in 2 lines separated by 1 line break
        test_frame._generate_layout_controllers()
        assert(len(test_frame.layout_controllers) == 2)
        assert(isinstance(test_frame.layout_controllers[1], AutoNewLine))
        assert(test_frame.layout_controllers[1].flowable_frame == test_frame)
        assert(test_frame.layout_controllers[1].x == live_width)

    def test_generate_layout_controllers_with_many_lines(self):
        live_width = brown.document.paper.live_width
        test_frame = FlowableFrame((Mm(0), Mm(0)), live_width * 3.5, Mm(50), Mm(5))
        # Should result in four lines separated by 3 line breaks
        test_frame._generate_layout_controllers()
        assert(len(test_frame.layout_controllers) == 4)
        assert(all(isinstance(c, AutoNewLine)
                   for c in test_frame.layout_controllers[1:]))
        assert(all(c.flowable_frame == test_frame
                   for c in test_frame.layout_controllers))
        assert(test_frame.layout_controllers[1].x == live_width)
        assert(test_frame.layout_controllers[2].x == live_width * 2)
        assert(test_frame.layout_controllers[3].x == live_width * 3)

    def test_generate_layout_controllers_with_two_pages(self):
        live_width = brown.document.paper.live_width
        test_frame = FlowableFrame((Mm(0), Mm(0)), live_width * 1.5, Mm(256), Mm(5))
        # Should result in two lines separated by one page break
        test_frame._generate_layout_controllers()
        assert(len(test_frame.layout_controllers) == 2)
        assert(isinstance(test_frame.layout_controllers[0], AutoNewPage))
        assert(test_frame.layout_controllers[1].flowable_frame == test_frame)
        assert(test_frame.layout_controllers[1].x == live_width)

    def test_generate_layout_controllers_with_many_pages(self):
        live_width = brown.document.paper.live_width
        test_frame = FlowableFrame((Mm(0), Mm(0)), live_width * 3.5, Mm(256), Mm(5))
        test_frame._generate_layout_controllers()
        assert(len(test_frame.layout_controllers) == 4)
        assert(all(isinstance(c, AutoNewPage)
                   for c in test_frame.layout_controllers))
        assert(all(c.flowable_frame == test_frame
                   for c in test_frame.layout_controllers))
        assert(test_frame.layout_controllers[1].x == live_width)
        assert(test_frame.layout_controllers[2].x == live_width * 2)
        assert(test_frame.layout_controllers[3].x == live_width * 3)

    def test_generate_layout_controllers_new_lines_have_padding(self):
        live_width = brown.document.paper.live_width
        test_frame = FlowableFrame((Mm(0), Mm(0)), live_width * 3.5, Mm(1000), Mm(5))
        test_frame._generate_layout_controllers()
        new_lines = [c for c in test_frame.layout_controllers
                     if isinstance(c, AutoNewLine)]
        assert(all(b.offset_y == test_frame.y_padding for b in new_lines))

    def test_generate_layout_controllers_new_pages_have_no_padding(self):
        live_width = brown.document.paper.live_width
        test_frame = FlowableFrame((Mm(0), Mm(0)), live_width * 3.5, Mm(1000), Mm(5))
        test_frame._generate_layout_controllers()
        new_pages = [c for c in test_frame.layout_controllers
                     if isinstance(c, AutoNewPage)]
        assert(all(b.offset_y == 0 for b in new_pages))

    # Space conversion tests ##################################################

    def test_map_to_doc_in_first_line(self):
        frame_pos = Point(Mm(10), Mm(11))
        test_frame = FlowableFrame(frame_pos, Mm(2500), Mm(100), Mm(20))
        test_pos = Point((Mm(100), Mm(40)))
        page_origin = brown.document._page_origin_in_doc_space(1)
        expected_x = page_origin.x + frame_pos.x + test_pos.x
        expected_y = brown.document.paper.margin_top + frame_pos.y + test_pos.y
        assert(test_frame._map_to_doc(test_pos) ==
               Point(expected_x, expected_y))

    def test_map_to_doc_second_line(self):
        frame_pos = Point(Mm(10), Mm(11))
        test_frame = FlowableFrame(frame_pos, Mm(2500), Mm(20), Mm(5))
        test_pos = Point(Mm(300), Mm(5))
        first_line_width = brown.document.paper.live_width - frame_pos.x
        expected_x = (test_pos.x - first_line_width +
                      brown.document.paper.margin_left)
        page_origin = brown.document._page_origin_in_doc_space(1)
        second_line_y = (frame_pos.y + test_frame.height +
                         test_frame.y_padding + page_origin.y)
        expected_y = second_line_y + test_pos.y
        assert(test_frame._map_to_doc(test_pos) ==
               Point(expected_x, expected_y))

    def test_map_to_doc_in_third_line(self):
        frame_pos = Point(Mm(17), Mm(11))
        test_frame = FlowableFrame(frame_pos, Mm(2500), Mm(15), Mm(5))
        test_pos = Point(Mm(350), Mm(5))
        first_line_width = brown.document.paper.live_width - frame_pos.x
        second_line_width = brown.document.paper.live_width
        page_origin = brown.document._page_origin_in_doc_space(1)
        expected_x = (test_pos.x - first_line_width - second_line_width +
                      page_origin.x)
        expected_y = (page_origin.y + frame_pos.y + test_pos.y +
                      ((test_frame.height + test_frame.y_padding) * 2))
        assert(test_frame._map_to_doc(test_pos) ==
               Point(expected_x, expected_y))

    def test_map_to_doc_on_second_page_first_line(self):
        frame_pos = Point(Mm(17), Mm(11))
        test_frame = FlowableFrame(frame_pos, Mm(2500), Mm(15), Mm(5))
        test_pos = Point(Mm(2100), Mm(0))
        live_width = brown.document.paper.live_width
        page_origin = brown.document._page_origin_in_doc_space(2)
        num_full_lines = 13
        expected_x_on_last_line = (test_pos.x - (live_width * num_full_lines) + frame_pos.x)
        expected_x = page_origin.x + expected_x_on_last_line
        expected_y = page_origin.y + test_pos.y
        assert(test_frame._map_to_doc(test_pos) ==
               Point(expected_x, expected_y))

    def test_map_to_doc_on_second_page_second_line(self):
        frame_pos = Point(Mm(17), Mm(11))
        test_frame = FlowableFrame(frame_pos, Mm(2500), Mm(15), Mm(5))
        test_pos = Point(Mm(2300), Mm(5))
        live_width = brown.document.paper.live_width
        page_origin = brown.document._page_origin_in_doc_space(2)
        num_full_lines = 14
        expected_x_on_last_line = (test_pos.x - (live_width * num_full_lines) + frame_pos.x)
        expected_x = page_origin.x + expected_x_on_last_line
        expected_y = (page_origin.y + test_pos.y + test_frame.height + test_frame.y_padding)
        assert(test_frame._map_to_doc(test_pos) ==
               Point(expected_x, expected_y))

    def test_map_to_doc_y_same_across_pages(self):
        test_frame = FlowableFrame((Mm(10), Mm(0)), Mm(10000), Mm(90), Mm(5))
        page_origin = brown.document._page_origin_in_doc_space(1)
        live_width = brown.document.paper.live_width
        line_and_padding_height = test_frame.height + test_frame.y_padding
        for i in range(12):
            y_val = test_frame._map_to_doc(
                (((live_width * i) + Mm(10)), Mm(0)))[1]
            line_on_page = i % 3
            expected = (page_origin[1] +
                        line_and_padding_height * line_on_page)
            self.assertAlmostEqual(y_val, expected)

    def test_map_to_doc_raises_out_of_bounds_correctly(self):
        test_frame = FlowableFrame((Mm(17), Mm(11)), Mm(500), Mm(15), Mm(5))
        with assert_raises(OutOfBoundsError):
            test_frame._map_to_doc((-1, 1))
        with assert_raises(OutOfBoundsError):
            test_frame._map_to_doc((1, -1))
        with assert_raises(OutOfBoundsError):
            test_frame._map_to_doc((Mm(12000), 1))
        with assert_raises(OutOfBoundsError):
            test_frame._map_to_doc((1, Mm(16)))

    def test_x_pos_rel_to_line_start(self):
        test_frame = FlowableFrame((Mm(10), Mm(0)), Mm(500), Mm(90), Mm(5))
        assert(test_frame._x_pos_rel_to_line_start(Mm(170)) == Mm(20))
        assert(test_frame._x_pos_rel_to_line_start(Mm(320)) == Mm(10))

    def test_dist_to_line_end(self):
        test_frame = FlowableFrame((Mm(10), Mm(0)), Mm(500), Mm(90), Mm(5))
        assert(test_frame._dist_to_line_end(Mm(170)) == Mm(-140))
        assert(test_frame._dist_to_line_end(Mm(320)) == Mm(-150))

    def test_last_break_at(self):
        test_frame = FlowableFrame((Mm(10), Mm(0)), Mm(500), Mm(90), Mm(5))
        assert(test_frame._last_break_at(Mm(140)) ==
               test_frame.layout_controllers[0])
        assert(test_frame._last_break_at(Mm(180)) ==
               test_frame.layout_controllers[1])

    def test_last_break_at_raises_out_of_bounds_when_needed(self):
        test_frame = FlowableFrame((Mm(10), Mm(0)), Mm(10000), Mm(90), Mm(5))
        with assert_raises(OutOfBoundsError):
            test_frame._last_break_at(Mm(10000000))
