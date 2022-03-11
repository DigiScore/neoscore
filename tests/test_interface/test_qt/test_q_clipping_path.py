import unittest

from PyQt5 import QtGui
from neoscore.interface.qt.q_clipping_path import QClippingPath


class TestQClippingPath(unittest.TestCase):
    def test_calculate_clipping_area_covering_full_path(self):
        painter_path = QtGui.QPainterPath()
        painter_path.lineTo(100, 200)
        expected_rect = painter_path.boundingRect()
        result_rect = QClippingPath.calculate_clipping_area(
            painter_path.boundingRect(), None, None, 0
        )
        assert result_rect.x() == expected_rect.x()
        assert result_rect.y() == expected_rect.y()
        assert result_rect.width() == expected_rect.width()
        assert result_rect.height() == expected_rect.height()

    def test_calculate_clipping_area_starting_in_path(self):
        painter_path = QtGui.QPainterPath()
        painter_path.lineTo(100, 200)
        result_rect = QClippingPath.calculate_clipping_area(
            painter_path.boundingRect(), 50, None, 0
        )
        assert result_rect.x() == 50
        assert result_rect.y() == painter_path.boundingRect().y()
        assert result_rect.width() == 50
        assert result_rect.height() == painter_path.boundingRect().height()

    def test_calculate_clipping_area_ending_in_path(self):
        painter_path = QtGui.QPainterPath()
        painter_path.lineTo(100, 200)
        result_rect = QClippingPath.calculate_clipping_area(
            painter_path.boundingRect(), None, 50, 0
        )
        assert result_rect.x() == 0
        assert result_rect.y() == painter_path.boundingRect().y()
        assert result_rect.width() == 50
        assert result_rect.height() == painter_path.boundingRect().height()

    def test_calculate_clipping_area_starting_and_ending_in_path(self):
        painter_path = QtGui.QPainterPath()
        painter_path.lineTo(100, 200)
        result_rect = QClippingPath.calculate_clipping_area(
            painter_path.boundingRect(), 25, 30, 0
        )
        assert result_rect.x() == 25
        assert result_rect.y() == painter_path.boundingRect().y()
        assert result_rect.width() == 30
        assert result_rect.height() == painter_path.boundingRect().height()
