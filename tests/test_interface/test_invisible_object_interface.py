import unittest

from PyQt5 import QtWidgets

from brown.core import brown
from brown.interface.invisible_object_interface import InvisibleObjectInterface


class TestInvisibleObjectInterface(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_init_without_parent(self):
        test_object = InvisibleObjectInterface((5, 6))
        assert(test_object.x == 5)
        assert(test_object._qt_object.x() == 5)
        assert(test_object.y == 6)
        assert(test_object._qt_object.y() == 6)
        # Check that emptiness flag was passed correctly
        # (Use a bitwise AND mask to check for the set flag
        # because Qt stores flags by bitwise OR-ing them)
        assert(int(test_object._qt_object.flags() &
                   QtWidgets.QGraphicsItem.ItemHasNoContents))

    def test_init_with_parent(self):
        test_parent = InvisibleObjectInterface((5, 6))
        test_child = InvisibleObjectInterface((5, 6), parent=test_parent)
        assert(test_child.parent == test_child._parent)
        assert(test_child._qt_object.parentItem() == test_child._parent._qt_object)
