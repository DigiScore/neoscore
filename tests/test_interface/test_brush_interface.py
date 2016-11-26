from nose.tools import assert_raises
import unittest

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from brown.interface.brush_interface import BrushInterface


class TestBrushInterface(unittest.TestCase):

    def test_init(self):
        brush = BrushInterface('#f00000')
        assert(isinstance(brush._qt_object, QtGui.QBrush))

    def test_color_with_rgb(self):
        color_tuple = (0, 255, 0)
        color_str = '#00ff00'
        brush = BrushInterface(color_tuple)
        assert(isinstance(brush._qt_object, QtGui.QBrush))
        # Test that color stored in _qt_object is in str form
        assert(brush._qt_object.color().name() == color_str.lower())
        assert(brush.color == color_str)

    def test_color_with_str(self):
        color_str = '#00ff00'
        brush = BrushInterface(color_str)
        assert(isinstance(brush._qt_object, QtGui.QBrush))
        assert(brush.color == color_str)

    def test_color_with_bad_rgb_tuple_len_fails(self):
        with assert_raises(TypeError):
            color_tuple = (0, 255)
            brush = BrushInterface(color_tuple)

    def test_color_with_nonsense_input_fails(self):
        with assert_raises(TypeError):
            nonsense_args = list('foo')
            brush = BrushInterface(nonsense_args)

    def test_change_passed_to_qt_object(self):
        color_str = '#00ff00'
        brush = BrushInterface(color_str)
        assert(brush._qt_object.color().name() == color_str.lower())
