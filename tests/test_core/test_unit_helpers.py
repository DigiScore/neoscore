import pytest

from neoscore.core.units import Unit, convert_all_to_unit


def test_convert_all_to_unit_simple_dict():
    iterable = {"a": 1, "b": Unit(2), "c": "h"}
    convert_all_to_unit(iterable, Unit)
    assert iterable["a"] == Unit(1)


def test_convert_all_to_unit_simple_list():
    iterable = [1, Unit(2), "b"]
    convert_all_to_unit(iterable, Unit)
    assert iterable[0] == Unit(1)


def test_convert_all_to_unit_list_in_list():
    iterable = [5, 6, [7, 8]]
    convert_all_to_unit(iterable, Unit)
    assert isinstance(iterable[2], list)
    assert isinstance(iterable[2][0], Unit)
    assert iterable[2][0] == Unit(7)


def test_convert_all_to_unit_tuple_in_list():
    iterable = [(5, 6), 2, 3]
    convert_all_to_unit(iterable, Unit)
    assert isinstance(iterable[0][0], Unit)
    assert isinstance(iterable[0], tuple)
    assert iterable[0][0] == Unit(5)


def test_convert_all_to_unit_dict_in_list():
    iterable = [5, 6, 2, {"b": 3}]
    convert_all_to_unit(iterable, Unit)
    assert isinstance(iterable[3], dict)
    assert isinstance(iterable[3]["b"], Unit)
    assert iterable[3]["b"] == Unit(3)


def test_convert_all_to_unit_list_in_dict():
    iterable = {"a": 5, "b": [6, 7]}
    convert_all_to_unit(iterable, Unit)
    assert isinstance(iterable["b"], list)
    assert isinstance(iterable["b"][0], Unit)
    assert iterable["b"][0] == Unit(6)


def test_convert_all_to_unit_tuple_in_dict():
    iterable = {"a": 5, "b": (6, 7)}
    convert_all_to_unit(iterable, Unit)
    assert isinstance(iterable["b"], tuple)
    assert isinstance(iterable["b"][0], Unit)
    assert iterable["b"][0] == Unit(6)


def test_convert_all_to_unit_dict_in_dict():
    iterable = {"a": 5, "b": {6: 7}}
    convert_all_to_unit(iterable, Unit)
    assert isinstance(iterable["b"], dict)
    assert isinstance(iterable["b"][6], Unit)
    assert iterable["b"][6] == Unit(7)


def test_convert_all_to_unit_handles_strings_correctly():
    iterable = {"a": 5, "b": ["abcd", 2]}
    convert_all_to_unit(iterable, Unit)
    assert isinstance(iterable["b"][1], Unit)
    assert iterable["b"][1] == Unit(2)
    assert iterable["b"][0] == "abcd"


def test_convert_all_to_unit_raises_error_on_bad_input():
    with pytest.raises(TypeError):
        convert_all_to_unit("invalid argument type", Unit)  # noqa
