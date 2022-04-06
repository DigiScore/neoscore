import pytest

from neoscore.core import neoscore
from neoscore.core.flowable import Flowable, OutOfBoundsError
from neoscore.core.paper import Paper
from neoscore.core.point import Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import Mm

from ..helpers import AppTest, assert_almost_equal


class TestFlowable(AppTest):
    def setUp(self):
        super().setUp()
        neoscore.document.paper = Paper(
            *[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]
        )
        # live_width == Mm(160)
        # live_height == Mm(257)

    def test_init(self):
        flowable = Flowable((Mm(10), Mm(11)), None, Mm(1000), Mm(100), Mm(5))
        assert flowable.pos == Point(Mm(10), Mm(11))
        assert flowable.x == Mm(10)
        assert flowable.y == Mm(11)
        assert flowable.breakable_length == Mm(1000)
        assert flowable.height == Mm(100)
        assert flowable.y_padding == Mm(5)

    def test_self_pos_manipulation(self):
        flowable = Flowable((Mm(10), Mm(11)), None, Mm(1000), Mm(100), Mm(5))
        flowable.x = Mm(20)
        assert flowable.pos.x == Mm(20)
        flowable.y = Mm(21)
        assert flowable.pos.y == Mm(21)

    def flowable_with_explicit_parent(self):
        page = neoscore.document.pages[1]
        parent = PositionedObject((Mm(22), Mm(33)), page)
        flowable = Flowable(
            (Mm(10), Mm(11)),
            parent=parent,
            length=Mm(1000),
            height=Mm(100),
            y_padding=Mm(5),
        )
        map_result = flowable.map_to_canvas(Point(Mm(4), Mm(5)))
        assert_almost_equal(
            map_result,
            Point(Mm(4) + Mm(10) + Mm(22) + page.x, Mm(5) + Mm(11) + Mm(33) + page.y),
        )

    def test_generate_layout_controllers_with_only_one_line(self):
        flowable = Flowable((Mm(9), Mm(11)), None, Mm(100), Mm(50), Mm(5))
        flowable._generate_layout_controllers()
        assert len(flowable.layout_controllers) == 1
        assert flowable.layout_controllers[0].flowable_x == Mm(0)
        assert flowable.layout_controllers[0].pos == Point(Mm(9), Mm(11))
        assert flowable.layout_controllers[0].page == neoscore.document.pages[0]

    def test_generate_layout_controllers_with_two_lines(self):
        live_width = neoscore.document.paper.live_width
        flowable = Flowable((Mm(0), Mm(0)), None, live_width * 1.5, Mm(50), Mm(5))
        # Should result in 2 lines separated by 1 line break
        flowable._generate_layout_controllers()
        assert len(flowable.layout_controllers) == 2
        assert flowable.layout_controllers[1].flowable_x == live_width
        assert flowable.layout_controllers[1].page == neoscore.document.pages[0]

    def test_generate_layout_controllers_with_many_lines(self):
        live_width = neoscore.document.paper.live_width
        flowable = Flowable((Mm(0), Mm(0)), None, live_width * 3.5, Mm(50), Mm(5))
        # Should result in four lines separated by 3 line breaks
        flowable._generate_layout_controllers()
        assert len(flowable.layout_controllers) == 4
        assert flowable.layout_controllers[1].flowable_x == live_width
        assert flowable.layout_controllers[2].flowable_x == live_width * 2
        assert flowable.layout_controllers[3].flowable_x == live_width * 3

    def test_generate_layout_controllers_with_two_pages(self):
        live_width = neoscore.document.paper.live_width
        flowable = Flowable((Mm(0), Mm(0)), None, live_width * 1.5, Mm(256), Mm(5))
        # Should result in two lines separated by one page break
        flowable._generate_layout_controllers()
        assert len(flowable.layout_controllers) == 2
        assert flowable.layout_controllers[1].flowable_x == live_width

    def test_generate_layout_controllers_with_many_pages(self):
        live_width = neoscore.document.paper.live_width
        flowable = Flowable((Mm(0), Mm(0)), None, live_width * 3.5, Mm(256), Mm(5))
        flowable._generate_layout_controllers()
        assert len(flowable.layout_controllers) == 4
        assert flowable.layout_controllers[1].flowable_x == live_width
        assert flowable.layout_controllers[2].flowable_x == live_width * 2
        assert flowable.layout_controllers[3].flowable_x == live_width * 3

    def test_generate_layout_controllers_new_lines_have_padding(self):
        live_width = neoscore.document.paper.live_width
        flowable = Flowable((Mm(0), Mm(0)), None, live_width * 3.5, Mm(1000), Mm(5))
        flowable._generate_layout_controllers()
        # Test that every NewLine which is not also a page break has the expected
        # y_padding from the flowable
        current_page = None
        for line in flowable.layout_controllers:
            if current_page != line.page:
                current_page = line.page
                continue
            assert line.margin_bottom == flowable.y_padding

    def test_generate_layout_controllers_on_new_pages_have_no_padding(self):
        live_width = neoscore.document.paper.live_width
        flowable = Flowable((Mm(0), Mm(0)), None, live_width * 3.5, Mm(1000), Mm(5))
        flowable._generate_layout_controllers()
        # Test that every NewLine which is also a page break
        # has no y_padding (is aligned with the top of the live page area)
        current_page = None
        for line in flowable.layout_controllers:
            if current_page == line.page:
                continue
            current_page = line.page
            assert line.margin_bottom == Mm(0)

    # For reference
    # page live width == Mm(160)
    # page live height == Mm(257)

    def test_x_pos_rel_to_line_start(self):
        flowable = Flowable((Mm(10), Mm(0)), None, Mm(500), Mm(90), Mm(5))
        assert flowable.dist_to_line_start(Mm(170)) == Mm(20)
        assert flowable.dist_to_line_start(Mm(320)) == Mm(10)

    def testdist_to_line_end(self):
        flowable = Flowable((Mm(10), Mm(0)), None, Mm(500), Mm(90), Mm(5))
        assert flowable.dist_to_line_end(Mm(170)) == Mm(-140)
        assert flowable.dist_to_line_end(Mm(320)) == Mm(-150)

    def testlast_break_at(self):
        flowable = Flowable((Mm(10), Mm(0)), None, Mm(500), Mm(90), Mm(5))
        assert flowable.last_break_at(Mm(140)) == flowable.layout_controllers[0]
        assert flowable.last_break_at(Mm(180)) == flowable.layout_controllers[1]

    def testlast_break_at_raises_out_of_bounds_when_needed(self):
        flowable = Flowable((Mm(10), Mm(0)), None, Mm(10000), Mm(90), Mm(5))
        with pytest.raises(OutOfBoundsError):
            flowable.last_break_at(Mm(10000000))
