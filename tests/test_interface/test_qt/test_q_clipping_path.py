import unittest

from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from brown.core import brown
from brown.interface.qt.q_clipping_path import QClippingPath
from brown.utils.units import Unit


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
            painter_path.boundingRect(), Unit(50), None, 0
        )
        assert result_rect.x() == 50
        assert result_rect.y() == painter_path.boundingRect().y()
        assert result_rect.width() == 50
        assert result_rect.height() == painter_path.boundingRect().height()

    def test_calculate_clipping_area_ending_in_path(self):
        painter_path = QtGui.QPainterPath()
        painter_path.lineTo(100, 200)
        result_rect = QClippingPath.calculate_clipping_area(
            painter_path.boundingRect(), None, Unit(50), 0
        )
        assert result_rect.x() == 0
        assert result_rect.y() == painter_path.boundingRect().y()
        assert result_rect.width() == 50
        assert result_rect.height() == painter_path.boundingRect().height()

    def test_calculate_clipping_area_starting_and_ending_in_path(self):
        painter_path = QtGui.QPainterPath()
        painter_path.lineTo(100, 200)
        result_rect = QClippingPath.calculate_clipping_area(
            painter_path.boundingRect(), Unit(25), Unit(30), 0
        )
        assert result_rect.x() == 25
        assert result_rect.y() == painter_path.boundingRect().y()
        assert result_rect.width() == 30
        assert result_rect.height() == painter_path.boundingRect().height()

    def test_hash_path(self):
        path_1 = QtGui.QPainterPath()
        path_1.lineTo(100, 200)
        hash_1 = QClippingPath.hash_path(path_1)
        # Identical paths hash identically
        path_2 = QtGui.QPainterPath()
        path_2.lineTo(100, 200)
        hash_2 = QClippingPath.hash_path(path_2)
        assert hash_1 == hash_2
        # Paths with different fill rules hash differently
        path_3 = QtGui.QPainterPath()
        path_3.setFillRule(Qt.FillRule.WindingFill)
        path_3.lineTo(100, 200)
        hash_3 = QClippingPath.hash_path(path_3)
        assert hash_1 != hash_3
        # Paths with different elements hash differently
        path_4 = QtGui.QPainterPath()
        path_4.lineTo(100, 200)
        path_4.lineTo(123, 123)
        hash_4 = QClippingPath.hash_path(path_4)
        assert hash_4 != hash_1

    def test_hash_transform(self):
        transform_1 = QtGui.QTransform()
        hash_1 = QClippingPath.hash_transform(transform_1)
        assert hash_1 == QClippingPath.hash_transform(QtGui.QTransform())
        transform_2 = QtGui.QTransform()
        transform_2.scale(0.1, 0.1)
        hash_2 = QClippingPath.hash_transform(transform_2)
        transform_3 = QtGui.QTransform()
        transform_3.rotate(20)
        hash_3 = QClippingPath.hash_transform(transform_3)
        transform_4 = QtGui.QTransform()
        transform_4.translate(1, 2)
        hash_4 = QClippingPath.hash_transform(transform_4)
        assert len(set([hash_1, hash_2, hash_3, hash_4])) == 4

    def test_hash_transformed_path(self):
        path = QtGui.QPainterPath()
        path.lineTo(100, 200)
        transform_1 = QtGui.QTransform()
        hash_1 = QClippingPath.hash_transformed_path(path, transform_1)
        transform_2 = QtGui.QTransform()
        transform_2.scale(0.1, 0.1)
        hash_2 = QClippingPath.hash_transformed_path(path, transform_2)
        assert hash_1 != hash_2
