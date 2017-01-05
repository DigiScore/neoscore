import os
import unittest

from brown.core import brown
from brown.utils.units import GraphicUnit
from brown.utils.point import Point
from brown.core.pen import Pen
from brown.core.brush import Brush
from brown.core.paper import Paper
from brown.utils.units import Mm
from brown.core.flowable_frame import FlowableFrame


from mock_graphic_object import MockGraphicObject


class TestGraphicObject(unittest.TestCase):

    def setUp(self):
        brown.setup(
            Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.frame = FlowableFrame((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))

    def test_init(self):
        mock_pen = Pen('#ffffff')
        mock_brush = Brush('#eeeeee')
        mock_parent = MockGraphicObject((10, 11), parent=None)
        grob = MockGraphicObject(
            (5, 6), GraphicUnit(7), mock_pen, mock_brush, mock_parent)
        assert(isinstance(grob.pos.x, GraphicUnit))
        assert(grob.pos.x == grob.x)
        assert(grob.x == GraphicUnit(5))
        assert(isinstance(grob.pos.y, GraphicUnit))
        assert(grob.pos.y == grob.y)
        assert(grob.y == GraphicUnit(6))
        assert(grob.breakable_width == GraphicUnit(7))
        assert(grob.parent == mock_parent)

    def test_pos_setter_enforces_graphic_units(self):
        grob = MockGraphicObject((5, 6))
        assert(isinstance(grob.pos.x, GraphicUnit))
        assert(isinstance(grob.pos.y, GraphicUnit))

    def test_pos_setter_changes_x(self):
        grob = MockGraphicObject((5, 6))
        grob.pos = Point(7, 8)
        assert(grob.pos.x == GraphicUnit(7))
        assert(grob.pos.y == GraphicUnit(8))

    def test_map_from_origin(self):
        item = MockGraphicObject((5, 6))
        relative_x, relative_y = MockGraphicObject.map_from_origin(item)
        assert(relative_x.value == 5)
        assert(relative_y.value == 6)

    def test_map_from_origin_thorugh_parent(self):
        parent = MockGraphicObject((100, 101))
        item = MockGraphicObject((5, 6), parent=parent)
        relative_x, relative_y = MockGraphicObject.map_from_origin(item)
        assert(relative_x.value == 105)
        assert(relative_y.value == 107)

    def test_map_between_items(self):
        source = MockGraphicObject((5, 6))
        destination = MockGraphicObject((100, 100))
        relative_x, relative_y = MockGraphicObject.map_between_items(source, destination)
        assert(relative_x.value == 95)
        assert(relative_y.value == 94)

    def test_map_between_items_thorugh_parent(self):
        parent = MockGraphicObject((100, 102))
        source = MockGraphicObject((5, 6))
        destination = MockGraphicObject((1, 1), parent=parent)
        relative_x, relative_y = MockGraphicObject.map_between_items(source, destination)
        assert(relative_x.value == 96)
        assert(relative_y.value == 97)

    def test_document_pos(self):
        test_object = MockGraphicObject((Mm(1), Mm(2)), Mm(50), parent=self.frame)
        expected_pos = (brown.document._page_origin_in_doc_space(1) +
                        Point(Mm(1), Mm(2)))
        self.assertEqual(test_object.document_pos, expected_pos)
