import unittest

from nose.tools import assert_raises

from brown.models.virtual_accidental import VirtualAccidental
from brown.models.virtual_accidental import InvalidAccidentalError


class TestVirtualAccidental(unittest.TestCase):

    def test_integer_conversion(self):
        assert(VirtualAccidental('f').value == -1)
        assert(VirtualAccidental('n').value == 0)
        assert(VirtualAccidental('s').value == 1)

    def test_none_preservation(self):
        assert(VirtualAccidental(None).value is None)

    def test_garbage_string_value(self):
        with assert_raises(InvalidAccidentalError):
            VirtualAccidental('jfasdklf')

    def test_garbage_int_value(self):
        with assert_raises(InvalidAccidentalError):
            VirtualAccidental(238904)

    def test_garbage_type_value(self):
        with assert_raises(InvalidAccidentalError):
            VirtualAccidental(['nonsense', 'input'])

    def test_value_as_str(self):
        input_types = ['f', 'n', 's', None]
        for case in input_types:
            assert(VirtualAccidental(case).value_as_str == case)

    def test__eq__(self):
        assert(VirtualAccidental('f') == VirtualAccidental('f'))
        assert(VirtualAccidental('n') == VirtualAccidental('n'))
        assert(VirtualAccidental('s') == VirtualAccidental('s'))

    def test__ne__(self):
        assert(VirtualAccidental('f') != VirtualAccidental('s'))
        assert(VirtualAccidental('n') != VirtualAccidental('f'))
        assert(VirtualAccidental('s') != VirtualAccidental('n'))
        assert(VirtualAccidental('s') != 'nonsense')

    def test__repr__(self):
        assert(VirtualAccidental('f').__repr__() == 'VirtualAccidental("f")')

    def test__hash__(self):
        self.assertEqual({VirtualAccidental('f'),
                          VirtualAccidental('f'),
                          VirtualAccidental('s')},

                         {VirtualAccidental('f'),
                          VirtualAccidental('s')})

    def test__lt__(self):
        assert(VirtualAccidental('f') < VirtualAccidental('n'))
        assert(not VirtualAccidental('f') < VirtualAccidental('f'))

    def test__gt__(self):
        assert(VirtualAccidental('s') > VirtualAccidental('n'))
        assert(not VirtualAccidental('f') > VirtualAccidental('f'))
