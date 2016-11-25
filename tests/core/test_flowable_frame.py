import pytest
import unittest

from brown.core.paper import Paper
from brown.core import brown
from brown.utils.units import Mm
from brown.utils.point import Point
from brown.core.flowable_frame import FlowableFrame, OutOfBoundsError
from brown.core.auto_new_line import AutoNewLine
from brown.core.auto_new_page import AutoNewPage


# TODO: Regularize these tests and ensure that they are testing what they
#       say they are!!!


class TestFlowableFrame(unittest.TestCase):

    def setUp(self):
        brown.setup(
            Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))

    def test_init(self):
        test_frame = FlowableFrame((Mm(10), Mm(11)),
                                   width=Mm(1000), height=Mm(100),
                                   y_padding=Mm(20))
        assert(test_frame.x == Mm(10))
        assert(test_frame.y == Mm(11))
        assert(test_frame.pos.x == Mm(10))
        assert(test_frame.pos.y == Mm(11))
        assert(test_frame.width == Mm(1000))
        assert(test_frame.height == Mm(100))
        assert(test_frame.y_padding == Mm(20))

    def test_self_pos_manipulation(self):
        test_frame = FlowableFrame((Mm(10), Mm(11)),
                                   width=Mm(1000), height=Mm(100),
                                   y_padding=Mm(20))
        test_frame.x = Mm(20)
        assert(test_frame.pos.x == Mm(20))
        assert(test_frame.x == Mm(20))
        test_frame.y = Mm(21)
        assert(test_frame.pos.y == Mm(21))
        assert(test_frame.y == Mm(21))


    # Layout generation tests #################################################

    def test_generate_auto_layout_controllers_with_only_one_line(self):
        test_frame = FlowableFrame((Mm(9), Mm(11)),
                                   width=Mm(100), height=Mm(50),
                                   y_padding=Mm(20))
        test_frame._generate_auto_layout_controllers()
        assert(len(test_frame.auto_layout_controllers) == 1)
        assert(test_frame.auto_layout_controllers[0].flowable_frame == test_frame)
        assert(test_frame.auto_layout_controllers[0].x == Mm(0))
        assert(test_frame.auto_layout_controllers[0].page_pos == Point(Mm(9), Mm(11)))

    # BELOW ARE BROKEN

    def test_generate_auto_layout_controllers_with_two_lines(self):
        live_width = brown.document.paper.live_width
        test_frame = FlowableFrame((Mm(0), Mm(0)),
                                   width=live_width * 1.5, height=Mm(50),
                                   y_padding=Mm(20))
        # Should result in 2 lines separated by 1 line break
        test_frame._generate_auto_layout_controllers()
        assert(len(test_frame.auto_layout_controllers) == 2)
        assert(isinstance(test_frame.auto_layout_controllers[1], AutoNewLine))
        assert(test_frame.auto_layout_controllers[1].flowable_frame == test_frame)
        assert(test_frame.auto_layout_controllers[1].x == live_width)

    def test_generate_auto_layout_controllers_with_many_lines(self):
        live_width = brown.document.paper.live_width
        test_frame = FlowableFrame((Mm(0), Mm(0)),
                                   width=live_width * 3.5, height=Mm(50),
                                   y_padding=Mm(20))
        # Should result in four lines separated by 3 line breaks
        test_frame._generate_auto_layout_controllers()
        assert(len(test_frame.auto_layout_controllers) == 4)
        assert(all(isinstance(c, AutoNewLine)
                   for c in test_frame.auto_layout_controllers[1:]))
        assert(all(c.flowable_frame == test_frame
                   for c in test_frame.auto_layout_controllers))
        assert(test_frame.auto_layout_controllers[1].x == live_width)
        assert(test_frame.auto_layout_controllers[2].x == live_width * 2)
        assert(test_frame.auto_layout_controllers[3].x == live_width * 3)

    def test_generate_auto_layout_controllers_with_two_pages(self):
        live_width = brown.document.paper.live_width
        test_frame = FlowableFrame((Mm(0), Mm(0)),
                                   width=live_width * 1.5, height=Mm(2800),
                                   y_padding=Mm(300))
        # Should result in two lines separated by one page break
        test_frame._generate_auto_layout_controllers()
        assert(len(test_frame.auto_layout_controllers) == 2)
        assert(isinstance(test_frame.auto_layout_controllers[0], AutoNewPage))
        assert(test_frame.auto_layout_controllers[1].flowable_frame == test_frame)
        assert(test_frame.auto_layout_controllers[1].x == live_width)

    def test_generate_auto_layout_controllers_with_many_pages(self):
        live_width = brown.document.paper.live_width
        test_frame = FlowableFrame((Mm(0), Mm(0)),
                                   width=live_width * 3.5, height=Mm(2800),
                                   y_padding=Mm(300))
        test_frame._generate_auto_layout_controllers()
        assert(len(test_frame.auto_layout_controllers) == 4)
        assert(all(isinstance(c, AutoNewPage)
                   for c in test_frame.auto_layout_controllers))
        assert(all(c.flowable_frame == test_frame
                   for c in test_frame.auto_layout_controllers))
        assert(test_frame.auto_layout_controllers[1].x == live_width)
        assert(test_frame.auto_layout_controllers[2].x == live_width * 2)
        assert(test_frame.auto_layout_controllers[3].x == live_width * 3)

    def test_generate_auto_layout_controllers_new_lines_have_padding(self):
        live_width = brown.document.paper.live_width
        test_frame = FlowableFrame((Mm(0), Mm(0)),
                                   width=live_width * 3.5, height=Mm(2800),
                                   y_padding=Mm(300))
        test_frame._generate_auto_layout_controllers()
        new_lines = [c for c in test_frame.auto_layout_controllers
                     if isinstance(c, AutoNewLine)]
        assert(all(b.offset_y == test_frame.y_padding
                   for b in new_lines))

    def test_generate_auto_layout_controllers_new_pages_have_no_padding(self):
        live_width = brown.document.paper.live_width
        test_frame = FlowableFrame((Mm(0), Mm(0)),
                                   width=live_width * 3.5, height=Mm(2800),
                                   y_padding=Mm(300))
        test_frame._generate_auto_layout_controllers()
        new_pages = [c for c in test_frame.auto_layout_controllers
                     if isinstance(c, AutoNewPage)]
        assert(all(b.offset_y == 0
                   for b in new_pages))

    # Space conversion tests ##################################################

    def test_local_space_to_doc_space_x_in_first_line(self):
        test_frame = FlowableFrame((Mm(10), Mm(11)),
                                   width=Mm(1000), height=Mm(100),
                                   y_padding=Mm(20))
        x_val = test_frame._local_space_to_doc_space((Mm(100), Mm(40))).x
        page_origin = brown.document._page_origin_in_doc_space(1)
        assert(x_val == page_origin[0] + 10 + 100)

    def test_local_space_to_doc_space_y_in_first_line(self):
        test_frame = FlowableFrame((Mm(10), Mm(11)),
                                   width=Mm(1000), height=Mm(100),
                                   y_padding=Mm(20))
        y_val = test_frame._local_space_to_doc_space((Mm(100), Mm(40))).y
        assert(y_val == Mm(40) + Mm(11) + brown.document.paper.margin_top)

    def test_local_space_to_doc_space_x_in_second_line(self):
        test_frame = FlowableFrame((Mm(17), Mm(11)),
                                   width=Mm(10000), height=Mm(20),
                                   y_padding=Mm(5))
        x_val = test_frame._local_space_to_doc_space((Mm(300), Mm(5))).x
        first_line_width = brown.document.paper.live_width - Mm(17)
        expected = (Mm(300) - first_line_width +
                    brown.document.paper.margin_left)
        assert(x_val == expected)

    def test_local_space_to_doc_space_y_in_second_line(self):
        test_frame = FlowableFrame((Mm(17), Mm(11)),
                                   width=Mm(10000), height=Mm(20),
                                   y_padding=Mm(5))
        local_x_val = Mm(300)
        local_y_val = Mm(5)
        y_val = test_frame._local_space_to_doc_space((local_x_val, local_y_val)).y
        page_origin = brown.document._page_origin_in_doc_space(1)
        second_line_y = (Mm(11) + test_frame.height + test_frame.y_padding +
                         page_origin[1])
        assert(y_val == second_line_y + local_y_val)

    def test_local_space_to_doc_space_x_in_third_line(self):
        test_frame = FlowableFrame((Mm(17), Mm(11)),
                                   width=Mm(10000), height=Mm(15),
                                   y_padding=Mm(5))
        x_val = test_frame._local_space_to_doc_space((Mm(350), Mm(5))).x
        first_line_width = brown.document.paper.live_width - Mm(17)
        second_line_width = brown.document.paper.live_width
        page_origin = brown.document._page_origin_in_doc_space(1)
        expected = (Mm(350) - first_line_width - second_line_width +
                    page_origin[0])
        assert(x_val == expected)

    def test_local_space_to_doc_space_y_in_third_line(self):
        test_frame = FlowableFrame((Mm(17), Mm(11)),
                                   width=Mm(10000), height=Mm(15),
                                   y_padding=Mm(5))
        y_val = test_frame._local_space_to_doc_space((Mm(350), Mm(5))).y
        page_origin = brown.document._page_origin_in_doc_space(1)
        expected = (page_origin[1] + Mm(11) + Mm(5) +
                    ((test_frame.height + test_frame.y_padding) * 2))
        assert(y_val == expected)

    def test_local_space_to_doc_space_x_on_second_page_first_line(self):
        test_frame = FlowableFrame((Mm(17), Mm(11)),
                                   width=Mm(10000), height=Mm(15),
                                   y_padding=Mm(5))
        x_val = test_frame._local_space_to_doc_space((Mm(2100), Mm(40))).x
        live_width = brown.document.paper.live_width
        page_origin = brown.document._page_origin_in_doc_space(2)
        num_full_lines = 13
        expected_x_on_last_line = (Mm(2100) - (live_width * num_full_lines) + Mm(17))
        expected = page_origin[0] + expected_x_on_last_line
        self.assertAlmostEqual(x_val, expected)

    def test_local_space_to_doc_space_y_on_second_page_first_line(self):
        test_frame = FlowableFrame((Mm(17), Mm(11)),
                                   width=Mm(100000), height=Mm(300),
                                   y_padding=Mm(5))
        y_val = test_frame._local_space_to_doc_space((Mm(16000), Mm(40))).y
        page_origin = brown.document._page_origin_in_doc_space(2)
        expected = page_origin[1] + Mm(40)
        self.assertAlmostEqual(y_val, expected)

    def test_local_space_to_doc_space_x_on_second_page_second_line(self):
        test_frame = FlowableFrame((Mm(17), Mm(11)),
                                   width=Mm(10000), height=Mm(15),
                                   y_padding=Mm(5))
        x_val = test_frame._local_space_to_doc_space((Mm(2300), Mm(40))).x
        live_width = brown.document.paper.live_width
        page_origin = brown.document._page_origin_in_doc_space(2)
        num_full_lines = 14
        expected_x_on_last_line = (Mm(2300) -
            (live_width * num_full_lines) + Mm(17))
        expected = page_origin[0] + expected_x_on_last_line
        self.assertAlmostEqual(x_val, expected)

    def test_local_space_to_doc_space_y_on_second_page_second_line(self):
        test_frame = FlowableFrame((Mm(17), Mm(11)),
                                   width=Mm(10000), height=Mm(15),
                                   y_padding=Mm(5))
        y_val = test_frame._local_space_to_doc_space((Mm(2300), Mm(5))).y
        page_origin = brown.document._page_origin_in_doc_space(2)
        expected = (page_origin[1] + Mm(5) +
                    test_frame.height + test_frame.y_padding)
        self.assertAlmostEqual(y_val, expected)

    def test_local_space_to_doc_space_y_same_across_pages(self):
        test_frame = FlowableFrame((Mm(10), Mm(0)),
                                   width=Mm(10000), height=Mm(90),
                                   y_padding=Mm(5))
        page_origin = brown.document._page_origin_in_doc_space(1)
        live_width = brown.document.paper.live_width
        line_and_padding_height = test_frame.height + test_frame.y_padding
        for i in range(12):
            y_val = test_frame._local_space_to_doc_space(
                (((live_width * i) + Mm(10)), Mm(0)))[1]
            line_on_page = i % 3
            expected = (page_origin[1] +
                        line_and_padding_height * line_on_page)
            self.assertAlmostEqual(y_val, expected)

    def test_local_space_to_doc_space_raises_out_of_bounds_correctly(self):
        test_frame = FlowableFrame((Mm(17), Mm(11)),
                                   width=Mm(10000), height=Mm(15),
                                   y_padding=Mm(5))
        with pytest.raises(OutOfBoundsError):
            test_frame._local_space_to_doc_space((-1, 1))
        with pytest.raises(OutOfBoundsError):
            test_frame._local_space_to_doc_space((1, -1))
        with pytest.raises(OutOfBoundsError):
            test_frame._local_space_to_doc_space((Mm(12000), 1))
        with pytest.raises(OutOfBoundsError):
            test_frame._local_space_to_doc_space((1, Mm(16)))

    def test_x_pos_rel_to_line_start(self):
        test_frame = FlowableFrame((Mm(10), Mm(0)),
                                   width=Mm(10000), height=Mm(90),
                                   y_padding=Mm(5))
        # brown.document.paper.live_width == Mm(160)
        assert(test_frame._x_pos_rel_to_line_start(Mm(170)) == Mm(20))
        assert(test_frame._x_pos_rel_to_line_start(Mm(320)) == Mm(10))

    def test_x_pos_rel_to_line_end(self):
        test_frame = FlowableFrame((Mm(10), Mm(0)),
                                   width=Mm(10000), height=Mm(90),
                                   y_padding=Mm(5))
        # brown.document.paper.live_width == Mm(160)
        assert(test_frame._x_pos_rel_to_line_end(Mm(170)) == Mm(-140))
        assert(test_frame._x_pos_rel_to_line_end(Mm(320)) == Mm(-150))

    def test_last_break_at(self):
        test_frame = FlowableFrame((Mm(10), Mm(0)),
                                   width=Mm(10000), height=Mm(90),
                                   y_padding=Mm(5))
        # brown.document.paper.live_width == Mm(160)
        assert(test_frame._last_break_at(Mm(140)) ==
               test_frame.auto_layout_controllers[0])
        assert(test_frame._last_break_at(Mm(180)) ==
               test_frame.auto_layout_controllers[1])

    def test_last_break_at_raises_out_of_bounds_when_needed(self):
        test_frame = FlowableFrame((Mm(10), Mm(0)),
                                   width=Mm(10000), height=Mm(90),
                                   y_padding=Mm(5))
        with pytest.raises(OutOfBoundsError):
            test_frame._last_break_at(Mm(10000000))
