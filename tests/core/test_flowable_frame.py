import pytest
import unittest

from brown.core.paper import Paper
from brown.core import brown
from brown.core.flowable_frame import FlowableFrame



class TestFlowableFrame(unittest.TestCase):

    def setUp(self):
        brown.setup(Paper(210, 297, 20, 20, 20, 20, 10))

    def test_init(self):
        test_frame = FlowableFrame(10, 11,
                                   width=1000, height=100,
                                   min_gap_below=20)
        assert(test_frame.x == 10)
        assert(test_frame.y == 11)
        assert(test_frame.width == 1000)
        assert(test_frame.height == 100)
        assert(test_frame.min_gap_below == 20)

    # Layout generation tests #################################################

    def test_generate_auto_layout_controllers_with_no_controllers_needed(self):
        test_frame = FlowableFrame(10, 11,
                                   width=200, height=50,
                                   min_gap_below=20)
        test_frame._generate_auto_layout_controllers()
        assert(len(test_frame.auto_layout_controllers) == 0)

    # Space conversion tests ##################################################

    @pytest.mark.skip
    def test_local_space_to_doc_space_x_in_first_span(self):
        test_frame = FlowableFrame(10, 11,
                                   width=1000, height=100,
                                   min_gap_below=20)
        x_val = test_frame._local_space_to_doc_space(100, 40)[0]
        assert(x_val == 100)
