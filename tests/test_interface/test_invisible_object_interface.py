import unittest

from PyQt5 import QtWidgets

from brown.core import brown
from brown.interface.invisible_object_interface import InvisibleObjectInterface


class TestInvisibleObjectInterface(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_init(self):
        test_object = InvisibleObjectInterface((5, 6))
        # Check that emptiness flag was passed correctly
        # (Use a bitwise AND mask to check for the set flag
        # because Qt stores flags by bitwise OR-ing them)
        assert(int(test_object._qt_object.flags() &
                   QtWidgets.QGraphicsItem.ItemHasNoContents))
