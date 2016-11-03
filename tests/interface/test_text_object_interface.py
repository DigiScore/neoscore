import unittest

from brown.core import brown
from brown.interface.text_object_interface import TextObjectInterface
from mock_graphic_object import MockGraphicObject
from brown.interface.font_interface import FontInterface


class TestTextObjectInterface(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_init(self):
        mock_parent = MockGraphicObject(None, 0, 0)
        test_font = FontInterface('Bravura', 12)
        test_object = TextObjectInterface(5, 6, 'testing',
                                          test_font, mock_parent)
        assert(test_object.x == 5)
        assert(test_object._qt_object.x() == 5)
        assert(test_object.y == 6)
        assert(test_object._qt_object.y() == 6)
        assert(test_object.text == 'testing')
        assert(test_object._qt_object.text() == test_object.text)
        assert(test_object.font == test_font)
        assert(test_object._qt_object.font() == test_object.font._qt_object)
        assert(test_object.parent == mock_parent)
        assert(test_object._qt_object.parentItem() == test_object.parent._qt_object)

    def test_text_setter_changes_qt_object(self):
        test_font = FontInterface('Bravura', 12)
        test_object = TextObjectInterface(5, 6, 'testing',
                                          test_font)
        test_object.text = 'new value'
        assert(test_object.text == 'new value')
        assert(test_object._qt_object.text() == 'new value')

    def test_font_setter_changes_qt_object(self):
        test_font = FontInterface('Bravura', 12)
        test_object = TextObjectInterface(5, 6, 'testing',
                                          test_font)
        new_test_font = FontInterface('Bravura', 16)
        test_object.font = new_test_font
        assert(test_object.font == new_test_font)
        assert(test_object._qt_object.font() == new_test_font._qt_object)
