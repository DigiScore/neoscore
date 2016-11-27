from nose.tools import assert_raises
import unittest

from brown.core import brown
from brown.core.paper import Paper
from brown.utils.units import Mm
from brown.core.flowable_frame import FlowableFrame
from brown.core.flowable_object import FlowableObject
from brown.utils.point import Point
from mock_flowable_object import MockFlowableObject


class TestFlowableObject(unittest.TestCase):

    def setUp(self):
        brown.setup(
            Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.frame = FlowableFrame((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))

    def test_init(self):
        test_object = MockFlowableObject((Mm(1), Mm(2)), Mm(50), self.frame)
        self.assertEqual(test_object._interfaces, [])
        self.assertEqual(test_object.pos, Point(Mm(1), Mm(2)))
        self.assertEqual(test_object.x, Mm(1))
        self.assertEqual(test_object.y, Mm(2))
        self.assertEqual(test_object.width, Mm(50))
        self.assertEqual(test_object.frame, self.frame)

    def test_document_pos(self):
        test_object = MockFlowableObject((Mm(1), Mm(2)), Mm(50), self.frame)
        expected_pos = (brown.document._page_origin_in_doc_space(1) +
                        Point(Mm(1), Mm(2)))
        self.assertEqual(test_object.document_pos, expected_pos)
