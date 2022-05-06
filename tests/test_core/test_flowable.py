from neoscore.core import neoscore
from neoscore.core.break_hint import BreakHint
from neoscore.core.flowable import Flowable
from neoscore.core.layout_controllers import MarginController
from neoscore.core.paper import Paper
from neoscore.core.point import ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Mm

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
        assert flowable.length == Mm(1000)
        assert flowable.height == Mm(100)
        assert flowable.y_padding == Mm(5)
        assert flowable.break_threshold == Mm(5)

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
        flowable._generate_lines()
        map_result = flowable.map_to_canvas(Point(Mm(4), Mm(5)))
        assert_almost_equal(
            map_result,
            Point(Mm(4) + Mm(10) + Mm(22) + page.x, Mm(5) + Mm(11) + Mm(33) + page.y),
        )

    def test_generate_layout_controllers_with_only_one_line(self):
        flowable = Flowable((Mm(9), Mm(11)), None, Mm(100), Mm(50), Mm(5))
        flowable._generate_lines()
        assert len(flowable.lines) == 1
        assert flowable.lines[0].flowable_x == Mm(0)
        assert flowable.lines[0].pos == Point(Mm(9), Mm(11))
        assert flowable.lines[0].page == neoscore.document.pages[0]

    def test_generate_layout_controllers_with_two_lines(self):
        live_width = neoscore.document.paper.live_width
        flowable = Flowable(ORIGIN, None, live_width * 1.5, Mm(50), Mm(5))
        flowable._generate_lines()
        # Should result in 2 lines separated by 1 line break
        flowable._generate_lines()
        assert len(flowable.lines) == 2
        assert flowable.lines[1].flowable_x == live_width
        assert flowable.lines[1].page == neoscore.document.pages[0]

    def test_generate_layout_controllers_with_many_lines(self):
        live_width = neoscore.document.paper.live_width
        flowable = Flowable(ORIGIN, None, live_width * 3.5, Mm(50), Mm(5))
        # Should result in four lines separated by 3 line breaks
        flowable._generate_lines()
        assert len(flowable.lines) == 4
        assert flowable.lines[1].flowable_x == live_width
        assert flowable.lines[2].flowable_x == live_width * 2
        assert flowable.lines[3].flowable_x == live_width * 3

    def test_generate_layout_controllers_with_two_pages(self):
        live_width = neoscore.document.paper.live_width
        flowable = Flowable(ORIGIN, None, live_width * 1.5, Mm(256), Mm(5))
        # Should result in two lines separated by one page break
        flowable._generate_lines()
        assert len(flowable.lines) == 2
        assert flowable.lines[1].flowable_x == live_width

    def test_generate_layout_controllers_with_many_pages(self):
        live_width = neoscore.document.paper.live_width
        flowable = Flowable(ORIGIN, None, live_width * 3.5, Mm(256), Mm(5))
        flowable._generate_lines()
        assert len(flowable.lines) == 4
        assert flowable.lines[1].flowable_x == live_width
        assert flowable.lines[2].flowable_x == live_width * 2
        assert flowable.lines[3].flowable_x == live_width * 3

    def test_generate_layout_controllers_with_break_opportunities(self):
        live_width = neoscore.document.paper.live_width
        flowable = Flowable(
            ORIGIN, None, live_width * 3, Mm(100), break_threshold=Mm(20)
        )
        BreakHint((live_width - Mm(21), ZERO), flowable)
        BreakHint((live_width - Mm(19), ZERO), flowable)
        flowable._generate_lines()
        assert flowable.lines[1].flowable_x == live_width - Mm(19)

    def test_generate_layout_controllers_with_margin_controllers(self):
        live_width = neoscore.document.paper.live_width
        flowable = Flowable((Mm(10), ZERO), None, live_width * 3, Mm(50))
        flowable.provided_controllers.add(MarginController(ZERO, Mm(20)))
        second_controller_x = Mm(160)
        flowable.provided_controllers.add(MarginController(second_controller_x, Mm(50)))
        other_layer_controller_x = Mm(300)
        flowable.provided_controllers.add(
            MarginController(other_layer_controller_x, Mm(10), "other layer")
        )
        flowable._generate_lines()
        assert flowable.lines[0].x == Mm(30)
        assert flowable.lines[1].x == Mm(20)
        assert flowable.lines[2].x == Mm(50)
        assert flowable.lines[3].x == Mm(60)

    def test_add_margin_controller_with_no_collision(self):
        flowable = Flowable((Mm(10), ZERO), None, Mm(500), Mm(50))
        flowable.add_margin_controller(MarginController(ZERO, Mm(20)))
        flowable.add_margin_controller(MarginController(ZERO, Mm(20), "other layer"))
        assert len(flowable.provided_controllers) == 2

    def test_add_margin_controller_with_collision(self):
        flowable = Flowable((Mm(10), ZERO), None, Mm(500), Mm(50))
        flowable.add_margin_controller(MarginController(ZERO, Mm(20)))
        flowable.add_margin_controller(MarginController(ZERO, Mm(10), "other layer"))
        flowable.add_margin_controller(MarginController(ZERO, Mm(20)))
        assert len(flowable.provided_controllers) == 2
        assert flowable.provided_controllers[0].margin_left == Mm(20)
        assert flowable.provided_controllers[1].margin_left == Mm(10)
        flowable.add_margin_controller(MarginController(ZERO, Mm(40)))
        assert len(flowable.provided_controllers) == 2
        assert flowable.provided_controllers[0].margin_left == Mm(10)
        assert flowable.provided_controllers[1].margin_left == Mm(40)

    # For reference
    # page live width == Mm(160)
    # page live height == Mm(257)

    def test_last_break_at(self):
        flowable = Flowable((Mm(10), Mm(0)), None, Mm(500), Mm(90), Mm(5))
        flowable._generate_lines()
        assert flowable.last_break_at(Mm(140)) == flowable.lines[0]
        assert flowable.last_break_at(Mm(180)) == flowable.lines[1]

    def test_last_break_at_raises_out_of_bounds_when_needed(self):
        flowable = Flowable((Mm(10), Mm(0)), None, Mm(10000), Mm(90), Mm(5))
        flowable._generate_lines()
        assert flowable.last_break_at(Mm(10000000)) == flowable.lines[-1]
