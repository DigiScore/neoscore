from nose.tools import assert_raises

from brown.models.virtual_accidental import VirtualAccidental
from brown.models.virtual_accidental import InvalidAccidentalError


def test_integer_conversion():
    assert(VirtualAccidental('f').value == -1)
    assert(VirtualAccidental('n').value == 0)
    assert(VirtualAccidental('s').value == 1)


def test_none_preservation():
    assert(VirtualAccidental(None).value is None)


def test_garbage_string_value():
    with assert_raises(InvalidAccidentalError):
        VirtualAccidental('jfasdklf')


def test_garbage_int_value():
    with assert_raises(InvalidAccidentalError):
        VirtualAccidental(238904)


def test_garbage_type_value():
    with assert_raises(InvalidAccidentalError):
        VirtualAccidental(['nonsense', 'input'])


def test_value_as_str():
    input_types = ['f', 'n', 's', None]
    for case in input_types:
        assert(VirtualAccidental(case).value_as_str == case)
