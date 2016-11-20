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
        grob = MockGraphicObject(
            (5, 6), mock_pen, mock_brush, mock_parent)
        assert(isinstance(grob.pos.x, GraphicUnit))
        assert(grob.pos.x == grob.x)
        assert(grob.x == GraphicUnit(5))
        assert(isinstance(grob.pos.y, GraphicUnit))
        assert(grob.pos.y == grob.y)
        assert(grob.y == GraphicUnit(6))
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

    def test_pen_setter_changes_pen_interface(self):
        # TODO: Make me!
        pass

    def test_brush_setter_changes_brush_interface(self):
        # TODO: Make me!
        pass

    def test_pos_relative_to_item(self):
        grob = MockGraphicObject((100, 100))
        other = MockGraphicObject((5, 6))
        relative_x, relative_y = grob.pos_relative_to_item(other)
        assert(relative_x.value == 95)
        assert(relative_y.value == 94)
