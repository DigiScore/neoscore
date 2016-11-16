import os
import unittest

from brown.core import brown
from brown.utils.graphic_unit import GraphicUnit
from brown.utils.point import Point
from brown.core.pen import Pen
from brown.core.brush import Brush

from mock_graphic_object import MockGraphicObject


class TestGraphicObject(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_init(self):
        mock_pen = Pen('#ffffff')
        mock_brush = Brush('#eeeeee')
        mock_parent = MockGraphicObject((10, 11), parent=None)
        test_object = MockGraphicObject(
            (5, 6), mock_pen, mock_brush, mock_parent)
        assert(isinstance(test_object.pos.x, GraphicUnit))
        assert(test_object.pos.x == test_object.x)
        assert(test_object.x == GraphicUnit(5))
        assert(isinstance(test_object.pos.y, GraphicUnit))
        assert(test_object.pos.y == test_object.y)
        assert(test_object.y == GraphicUnit(6))
        assert(test_object.parent == mock_parent)

    def test_pos_setter_enforces_graphic_units(self):
        test_object = MockGraphicObject((5, 6))
        assert(isinstance(test_object.pos.x, GraphicUnit))
        assert(isinstance(test_object.pos.y, GraphicUnit))

    def test_pos_setter_changes_x(self):
        test_object = MockGraphicObject((5, 6))
        test_object.pos = Point(7, 8)
        assert(test_object.pos.x == GraphicUnit(7))
        assert(test_object.pos.y == GraphicUnit(8))

    def test_pen_setter_changes_pen_interface(self):
        # TODO: Make me!
        pass

    def test_brush_setter_changes_brush_interface(self):
        # TODO: Make me!
        pass
