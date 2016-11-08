import pytest
import unittest

from brown.core import brown
from brown.core.flowable_frame import FlowableFrame



class TestFlowableFrame(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_init(self):
        test_frame = FlowableFrame(10, 11, document=None,
                                   width=1000, height=100,
                                   default_span_width=300)
        assert(test_frame.x == 10)
        assert(test_frame.y == 11)
        assert(test_frame.width == 1000)
        assert(test_frame.height == 100)
        # TODO: once doc is implemented test it
        assert(test_frame.document is None)

    def test_span_width_at(self):
        test_frame = FlowableFrame(10, 11, document=None,
                                   width=1000, height=100,
                                   default_span_width=300)
        assert(test_frame._span_width_at(100) == 300)

    # Space conversion tests ##################################################

    def test_local_space_to_doc_space_x_in_first_span(self):
        test_frame = FlowableFrame(10, 11, document=None,
                                   width=1000, height=100, default_span_width=300)
        x_val = test_frame._local_space_to_doc_space(100, 40)[0]
        assert(x_val == 100)
