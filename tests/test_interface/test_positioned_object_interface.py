from PyQt5.QtWidgets import QGraphicsSimpleTextItem

from neoscore.core.point import ORIGIN
from neoscore.interface.positioned_object_interface import PositionedObjectInterface

from ..helpers import AppTest


class TestPositionedObjectInterface(AppTest):
    def test_register_qt_object_without_parent(self):
        interface = PositionedObjectInterface(ORIGIN, None, 1, 0, ORIGIN)
        assert not hasattr(interface, "_qt_object")
        qt_obj = QGraphicsSimpleTextItem()
        interface._register_qt_object(qt_obj)
        assert interface._qt_object == qt_obj
        assert qt_obj.parentItem() is None
        assert qt_obj.scene() is not None

    def test_register_qt_object_with_parent(self):
        parent_interface = PositionedObjectInterface(ORIGIN, None, 1, 0, ORIGIN)
        parent_interface._register_qt_object(QGraphicsSimpleTextItem())
        interface = PositionedObjectInterface(ORIGIN, parent_interface, 1, 0, ORIGIN)
        qt_obj = QGraphicsSimpleTextItem()
        interface._register_qt_object(qt_obj)
        assert qt_obj.parentItem() == parent_interface._qt_object
        assert qt_obj.scene() is not None
