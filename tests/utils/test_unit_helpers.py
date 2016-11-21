import pytest
import unittest


from brown.utils.units_helpers import (
    convert_contents_to_unit_in_place,
    recursively_convert_contents_to_unit_in_place,
)
from brown.utils.graphic_unit import GraphicUnit


def test_convert_contents_to_unit_in_place():
    working_list = [1, 2]
    convert_contents_to_unit_in_place(working_list, GraphicUnit)
    assert(all(isinstance(el, GraphicUnit) for el in working_list))
    assert(working_list[0] == GraphicUnit(1))
    assert(working_list[1] == GraphicUnit(2))


def test_convert_contents_to_unit_in_place_with_non_numerical_elements():
    working_list = [1, 2, 'foo']
    convert_contents_to_unit_in_place(working_list, GraphicUnit)
    assert(working_list[0] == GraphicUnit(1))
    assert(working_list[1] == GraphicUnit(2))


def test_recursively_convert_contents_to_unit_in_place_simple_dict():
    iterable = {'a': 1, 'b': 2, 'c': 3}
    recursively_convert_contents_to_unit_in_place(iterable, GraphicUnit)
    assert(iterable['a'] == GraphicUnit(1))


def test_recursively_convert_contents_to_unit_in_place_simple_list():
    iterable = [1, 2, 3]
    recursively_convert_contents_to_unit_in_place(iterable, GraphicUnit)
    assert(iterable[0] == GraphicUnit(1))


def test_recursively_convert_contents_to_unit_in_place_list_in_list():
    iterable = [5, 6, [7, 8]]
    recursively_convert_contents_to_unit_in_place(iterable, GraphicUnit)
    assert(isinstance(iterable[2], list))
    assert(isinstance(iterable[2][0], GraphicUnit))
    assert(iterable[2][0] == GraphicUnit(7))


def test_recursively_convert_contents_to_unit_in_place_tuple_in_list():
    iterable = [(5, 6), 2, 3]
    recursively_convert_contents_to_unit_in_place(iterable, GraphicUnit)
    assert(isinstance(iterable[0][0], GraphicUnit))
    assert(isinstance(iterable[0], tuple))
    assert(iterable[0][0] == GraphicUnit(5))


def test_recursively_convert_contents_to_unit_in_place_dict_in_list():
    iterable = [5, 6, 2, {'b': 3}]
    recursively_convert_contents_to_unit_in_place(iterable, GraphicUnit)
    assert(isinstance(iterable[3], dict))
    assert(isinstance(iterable[3]['b'], GraphicUnit))
    assert(iterable[3]['b'] == GraphicUnit(3))


def test_recursively_convert_contents_to_unit_in_place_list_in_dict():
    iterable = {'a': 5, 'b': [6, 7]}
    recursively_convert_contents_to_unit_in_place(iterable, GraphicUnit)
    assert(isinstance(iterable['b'], list))
    assert(isinstance(iterable['b'][0], GraphicUnit))
    assert(iterable['b'][0] == GraphicUnit(6))


def test_recursively_convert_contents_to_unit_in_place_tuple_in_dict():
    iterable = {'a': 5, 'b': (6, 7)}
    recursively_convert_contents_to_unit_in_place(iterable, GraphicUnit)
    assert(isinstance(iterable['b'], tuple))
    assert(isinstance(iterable['b'][0], GraphicUnit))
    assert(iterable['b'][0] == GraphicUnit(6))


def test_recursively_convert_contents_to_unit_in_place_dict_in_dict():
    iterable = {'a': 5, 'b': {6: 7}}
    recursively_convert_contents_to_unit_in_place(iterable, GraphicUnit)
    assert(isinstance(iterable['b'], dict))
    assert(isinstance(iterable['b'][6], GraphicUnit))
    assert(iterable['b'][6] == GraphicUnit(7))
