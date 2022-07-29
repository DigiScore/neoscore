from PyQt5.QtGui import QColor, QPainterPath, QPen

from neoscore.interface.qt.q_clipping_path import QClippingPath

from ...helpers import AppTest


class TestQClippingPath(AppTest):
    def setUp(self):
        super().setUp()
        self.pen = QPen(QColor("#000000"), 2)
        self.pen_padding_width = self.pen.widthF() / 2

    def test_clip_measurements_scale_adjusted(self):
        painter_path = QPainterPath()
        obj = QClippingPath(painter_path, 2, 8, 2)
        assert obj.clip_start_x == 1
        assert obj.clip_width == 4

    def test_geometry_covering_full_path(self):
        painter_path = QPainterPath()
        painter_path.moveTo(-5, -5)
        painter_path.lineTo(100, 200)
        obj = QClippingPath(painter_path, 0, None)
        obj.setPen(self.pen)
        obj.update_geometry()
        # bounding rect should match that of the path plus padding for the pen width
        raw_path_rect = painter_path.boundingRect()
        assert obj.boundingRect().x() == raw_path_rect.x() - self.pen_padding_width
        assert obj.boundingRect().y() == raw_path_rect.y() - self.pen_padding_width
        assert obj.boundingRect().width() == raw_path_rect.width() + 5 + (
            self.pen_padding_width * 2
        )
        assert obj.boundingRect().height() == raw_path_rect.height() + (
            self.pen_padding_width * 2
        )
        assert obj.clip_rect == obj.boundingRect()

    def test_geometry_covering_end_of_path(self):
        painter_path = QPainterPath()
        painter_path.moveTo(-5, -5)
        painter_path.lineTo(100, 200)
        obj = QClippingPath(painter_path, 50, None)
        obj.setPen(self.pen)
        obj.update_geometry()
        raw_path_rect = painter_path.boundingRect()
        assert obj.boundingRect().x() == raw_path_rect.x()
        assert obj.boundingRect().y() == raw_path_rect.y() - self.pen_padding_width
        assert (
            obj.boundingRect().width()
            == raw_path_rect.width() + 5 - 50 + self.pen_padding_width
        )
        assert obj.boundingRect().height() == raw_path_rect.height() + (
            self.pen_padding_width * 2
        )
        assert obj.clip_rect == obj.boundingRect().translated(50, 0)

    def test_geometry_covering_start_of_path(self):
        painter_path = QPainterPath()
        painter_path.moveTo(-5, -5)
        painter_path.lineTo(100, 200)
        obj = QClippingPath(painter_path, 0, 50)
        obj.setPen(self.pen)
        obj.update_geometry()
        raw_path_rect = painter_path.boundingRect()
        assert obj.boundingRect().x() == raw_path_rect.x() - self.pen_padding_width
        assert obj.boundingRect().y() == raw_path_rect.y() - self.pen_padding_width
        assert obj.boundingRect().width() == 50 + 5 + self.pen_padding_width
        assert obj.boundingRect().height() == raw_path_rect.height() + (
            self.pen_padding_width * 2
        )
        assert obj.clip_rect == obj.boundingRect()

    def test_geometry_covering_middle_of_path(self):
        painter_path = QPainterPath()
        painter_path.moveTo(-5, -5)
        painter_path.lineTo(100, 200)
        obj = QClippingPath(painter_path, 25, 30)
        obj.setPen(self.pen)
        obj.update_geometry()
        raw_path_rect = painter_path.boundingRect()
        assert obj.boundingRect().x() == raw_path_rect.x()
        assert obj.boundingRect().y() == raw_path_rect.y() - self.pen_padding_width
        assert obj.boundingRect().width() == 30 + 5
        assert obj.boundingRect().height() == raw_path_rect.height() + (
            self.pen_padding_width * 2
        )
        assert obj.clip_rect == obj.boundingRect().translated(25, 0)
