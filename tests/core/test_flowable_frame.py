import pytest
import unittest

from brown.utils import units
from brown.core.paper import Paper
from brown.core import brown
from brown.core.flowable_frame import FlowableFrame
from brown.core.auto_line_break import AutoLineBreak
from brown.core.auto_page_break import AutoPageBreak



class TestFlowableFrame(unittest.TestCase):

    def setUp(self):
        brown.setup(Paper(210, 297, 20, 20, 20, 20, 10))

    def test_init(self):
        test_frame = FlowableFrame(10, 11,
                                   width=1000, height=100,
                                   y_padding=20)
        assert(test_frame.x == 10)
        assert(test_frame.y == 11)
        assert(test_frame.width == 1000)
        assert(test_frame.height == 100)
        assert(test_frame.y_padding == 20)

    # Layout generation tests #################################################

    def test_generate_auto_layout_controllers_with_no_controllers_needed(self):
        test_frame = FlowableFrame(10, 11,
                                   width=200, height=50,
                                   y_padding=20)
        test_frame._generate_auto_layout_controllers()
        assert(len(test_frame.auto_layout_controllers) == 0)

    def test_generate_auto_layout_controllers_with_one_line_break(self):
        live_width = brown.document.paper.live_width * units.mm
        test_frame = FlowableFrame(0, 0,
                                   width=live_width * 1.5, height=50,
                                   y_padding=20)
        # Should result in 2 lines separated by 1 line break
        test_frame._generate_auto_layout_controllers()
        assert(len(test_frame.auto_layout_controllers) == 1)
        assert(isinstance(test_frame.auto_layout_controllers[0], AutoLineBreak))
        assert(test_frame.auto_layout_controllers[0].flowable_frame == test_frame)
        assert(test_frame.auto_layout_controllers[0].x == live_width)

    def test_generate_auto_layout_controllers_with_many_line_breaks(self):
        live_width = brown.document.paper.live_width * units.mm
        test_frame = FlowableFrame(0, 0,
                                   width=live_width * 3.5, height=50,
                                   y_padding=20)
        # Should result in four lines separated by 3 line breaks
        test_frame._generate_auto_layout_controllers()
        assert(len(test_frame.auto_layout_controllers) == 3)
        assert(all(isinstance(c, AutoLineBreak)
                   for c in test_frame.auto_layout_controllers))
        assert(all(c.flowable_frame == test_frame
                   for c in test_frame.auto_layout_controllers))
        assert(test_frame.auto_layout_controllers[0].x == live_width)
        assert(test_frame.auto_layout_controllers[1].x == live_width * 2)
        assert(test_frame.auto_layout_controllers[2].x == live_width * 3)

    def test_generate_auto_layout_controllers_with_one_page_break(self):
        # brown.document.paper.live_height * units.mm == 1889.763779527559
        live_width = brown.document.paper.live_width * units.mm    # 3035.433070866142
        test_frame = FlowableFrame(0, 0,
                                   width=live_width * 1.5, height=2800,
                                   y_padding=300)
        # Should result in two lines separated by one page break
        test_frame._generate_auto_layout_controllers()
        assert(len(test_frame.auto_layout_controllers) == 1)
        assert(isinstance(test_frame.auto_layout_controllers[0], AutoPageBreak))
        assert(test_frame.auto_layout_controllers[0].flowable_frame == test_frame)
        assert(test_frame.auto_layout_controllers[0].x == live_width)

    def test_generate_auto_layout_controllers_with_many_page_breaks(self):
        # brown.document.paper.live_height * units.mm == 1889.763779527559
        live_width = brown.document.paper.live_width * units.mm    # 3035.433070866142
        test_frame = FlowableFrame(0, 0,
                                   width=live_width * 3.5, height=2800,
                                   y_padding=300)
        # Should result in two lines separated by one page break
        test_frame._generate_auto_layout_controllers()
        assert(len(test_frame.auto_layout_controllers) == 3)
        assert(all(isinstance(c, AutoPageBreak)
                   for c in test_frame.auto_layout_controllers))
        assert(all(c.flowable_frame == test_frame
                   for c in test_frame.auto_layout_controllers))
        assert(test_frame.auto_layout_controllers[0].x == live_width)
        assert(test_frame.auto_layout_controllers[1].x == live_width * 2)
        assert(test_frame.auto_layout_controllers[2].x == live_width * 3)

    def test_generate_auto_layout_controllers_line_breaks_have_padding(self):
        # brown.document.paper.live_height * units.mm == 1889.763779527559
        live_width = brown.document.paper.live_width * units.mm    # 3035.433070866142
        test_frame = FlowableFrame(0, 0,
                                   width=live_width * 3.5, height=2800,
                                   y_padding=300)
        # Should result in two lines separated by one page break
        test_frame._generate_auto_layout_controllers()
        line_breaks = [c for c in test_frame.auto_layout_controllers
                       if isinstance(c, AutoLineBreak)]
        assert(all(b.margin_above_next == test_frame.y_padding
                   for b in line_breaks))

    def test_generate_auto_layout_controllers_page_breaks_have_no_padding(self):
        # brown.document.paper.live_height * units.mm == 1889.763779527559
        live_width = brown.document.paper.live_width * units.mm    # 3035.433070866142
        test_frame = FlowableFrame(0, 0,
                                   width=live_width * 3.5, height=2800,
                                   y_padding=300)
        # Should result in two lines separated by one page break
        test_frame._generate_auto_layout_controllers()
        page_breaks = [c for c in test_frame.auto_layout_controllers
                       if isinstance(c, AutoPageBreak)]
        assert(all(b.margin_above_next == 0
                   for b in page_breaks))

    # Space conversion tests ##################################################

    def test_local_space_to_doc_space_x_in_first_line(self):
        test_frame = FlowableFrame(10, 11,
                                   width=1000, height=100,
                                   y_padding=20)
        x_val = test_frame._local_space_to_doc_space(100, 40)[0]
        page_origin = brown.document._page_origin_in_doc_space(1)
        assert(x_val == page_origin[0] + 10 + 100)

    def test_local_space_to_doc_space_y_in_first_line(self):
        test_frame = FlowableFrame(10, 11,
                                   width=1000, height=100,
                                   y_padding=20)
        y_val = test_frame._local_space_to_doc_space(100, 40)[1]
        assert(y_val == 40 + 11 + (brown.document.paper.margin_top * units.mm))

    def test_local_space_to_doc_space_x_in_second_line(self):
        test_frame = FlowableFrame(17, 11,
                                   width=10000, height=300,
                                   y_padding=80)
        x_val = test_frame._local_space_to_doc_space(3000, 40)[0]
        first_line_width = (brown.document.paper.live_width * units.mm) - 17
        expected = (3000 - first_line_width +
                    (brown.document.paper.margin_left * units.mm))
        assert(x_val == expected)

    def test_local_space_to_doc_space_y_in_second_line(self):
        test_frame = FlowableFrame(17, 11,
                                   width=10000, height=300,
                                   y_padding=80)
        y_val = test_frame._local_space_to_doc_space(3000, 40)[1]
        page_origin = brown.document._page_origin_in_doc_space(1)
        second_line_y = (11 + test_frame.height + test_frame.y_padding +
                         page_origin[1])
        assert(y_val == second_line_y + 40)

    def test_local_space_to_doc_space_x_in_third_line(self):
        test_frame = FlowableFrame(17, 11,
                                   width=10000, height=300,
                                   y_padding=80)
        x_val = test_frame._local_space_to_doc_space(5000, 40)[0]
        first_line_width = (brown.document.paper.live_width * units.mm) - 17
        second_line_width = (brown.document.paper.live_width * units.mm)
        expected = (5000 - first_line_width - second_line_width +
                    (brown.document.paper.margin_left * units.mm))
        assert(x_val == expected)

    @pytest.mark.skip
    def test_local_space_to_doc_space_y_in_third_line(self):
        test_frame = FlowableFrame(17, 11,
                                   width=10000, height=300,
                                   y_padding=80)
        y_val = test_frame._local_space_to_doc_space(6000, 40)[1]
        assert(y_val == 40 + 11 + (brown.document.paper.margin_top * units.mm))
