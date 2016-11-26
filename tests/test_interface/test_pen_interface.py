import pytest
import unittest

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from brown.interface.pen_interface import PenInterface


class TestPenInterface(unittest.TestCase):

    def test_init(self):
        pen = PenInterface('#f00000')
        assert(isinstance(pen._qt_object, QtGui.QPen))

    def test_color_with_rgb(self):
        color_tuple = (0, 255, 0)
        color_str = '#00ff00'
        pen = PenInterface(color_tuple)
        assert(isinstance(pen._qt_object, QtGui.QPen))
        # Test that color stored in _qt_object is in str form
        assert(pen._qt_object.color().name() == color_str.lower())
        assert(pen.color == color_str)

    def test_color_with_str(self):
        color_str = '#00ff00'
        pen = PenInterface(color_str)
        assert(isinstance(pen._qt_object, QtGui.QPen))
        assert(pen.color == color_str)

    def test_color_with_bad_rgb_tuple_len_fails(self):
        with pytest.raises(TypeError):
            color_tuple = (0, 255)
            pen = PenInterface(color_tuple)

    def test_color_with_nonsense_input_fails(self):
        with pytest.raises(TypeError):
            nonsense_args = list('foo')
            pen = PenInterface(nonsense_args)

    def test_change_passed_to_qt_object(self):
        color_str = '#00ff00'
        pen = PenInterface(color_str)
        assert(pen._qt_object.color().name() == color_str.lower())
