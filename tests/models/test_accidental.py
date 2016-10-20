import pytest

from brown.models.accidental import Accidental, InvalidAccidentalError


def test_integer_conversion():
    assert(Accidental('f').value == -1)
    assert(Accidental('n').value == 0)
    assert(Accidental('s').value == 1)


def test_none_preservation():
    assert(Accidental(None).value is None)


def test_garbage_string_value():
    with pytest.raises(InvalidAccidentalError):
        Accidental('jfasdklf')


def test_garbage_int_value():
    with pytest.raises(InvalidAccidentalError):
        Accidental(238904)


def test_garbage_type_value():
    with pytest.raises(InvalidAccidentalError):
        Accidental(['nonsense', 'input'])
