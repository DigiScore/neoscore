import unittest

from PyQt5 import QtGui

from brown.core import brown
from brown.interface.qt_ext.q_clipping_path import QClippingPath



class TestQClippingPath(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.pen_with_zero_width = QtGui.QPen()
        self.pen_with_zero_width.setWidth(0)

    def test_create_clipping_area_covering_full_path(self):
        painter_path = QtGui.QPainterPath()
        painter_path.lineTo(100, 200)
        path_item = QClippingPath(painter_path, 0, 500)
        path_item.setPen(self.pen_with_zero_width)
        expected_rect = painter_path.boundingRect()
        result_rect = path_item._create_clipping_area(painter_path, None, None)
        assert(result_rect.x() == expected_rect.x())
        assert(result_rect.y() == expected_rect.y())
        assert(result_rect.width() == expected_rect.width())
        assert(result_rect.height() == expected_rect.height())

    def test_create_clipping_area_starting_in_path(self):
        painter_path = QtGui.QPainterPath()
        painter_path.lineTo(100, 200)
        path_item = QClippingPath(painter_path, 0, 500)
        path_item.setPen(self.pen_with_zero_width)
        result_rect = path_item._create_clipping_area(painter_path, 50, None)
        assert(result_rect.x() == 50)
        assert(result_rect.y() == painter_path.boundingRect().y())
        assert(result_rect.width() == 50)
        assert(result_rect.height() == painter_path.boundingRect().height())

    def test_create_clipping_area_ending_in_path(self):
        painter_path = QtGui.QPainterPath()
        painter_path.lineTo(100, 200)
        path_item = QClippingPath(painter_path, 0, 500)
        path_item.setPen(self.pen_with_zero_width)
        result_rect = path_item._create_clipping_area(painter_path, None, 50)
        assert(result_rect.x() == 0)
        assert(result_rect.y() == painter_path.boundingRect().y())
        assert(result_rect.width() == 50)
        assert(result_rect.height() == painter_path.boundingRect().height())

    def test_create_clipping_area_starting_and_ending_in_path(self):
        painter_path = QtGui.QPainterPath()
        painter_path.lineTo(100, 200)
        path_item = QClippingPath(painter_path, 0, 500)
        path_item.setPen(self.pen_with_zero_width)
        result_rect = path_item._create_clipping_area(painter_path, 25, 30)
        assert(result_rect.x() == 25)
        assert(result_rect.y() == painter_path.boundingRect().y())
        assert(result_rect.width() == 30)
        assert(result_rect.height() == painter_path.boundingRect().height())
