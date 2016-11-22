from brown.utils.units import convert_all_to_unit
from brown.utils.units import GraphicUnit


def test_convert_all_to_unit_simple_dict():
    iterable = {'a': 1, 'b': 2, 'c': 3}
    convert_all_to_unit(iterable, GraphicUnit)
    assert(iterable['a'] == GraphicUnit(1))


def test_convert_all_to_unit_simple_list():
    iterable = [1, 2, 3]
    convert_all_to_unit(iterable, GraphicUnit)
    assert(iterable[0] == GraphicUnit(1))


def test_convert_all_to_unit_list_in_list():
    iterable = [5, 6, [7, 8]]
    convert_all_to_unit(iterable, GraphicUnit)
    assert(isinstance(iterable[2], list))
    assert(isinstance(iterable[2][0], GraphicUnit))
    assert(iterable[2][0] == GraphicUnit(7))


def test_convert_all_to_unit_tuple_in_list():
    iterable = [(5, 6), 2, 3]
    convert_all_to_unit(iterable, GraphicUnit)
    assert(isinstance(iterable[0][0], GraphicUnit))
    assert(isinstance(iterable[0], tuple))
    assert(iterable[0][0] == GraphicUnit(5))


def test_convert_all_to_unit_dict_in_list():
    iterable = [5, 6, 2, {'b': 3}]
    convert_all_to_unit(iterable, GraphicUnit)
    assert(isinstance(iterable[3], dict))
    assert(isinstance(iterable[3]['b'], GraphicUnit))
    assert(iterable[3]['b'] == GraphicUnit(3))


def test_convert_all_to_unit_list_in_dict():
    iterable = {'a': 5, 'b': [6, 7]}
    convert_all_to_unit(iterable, GraphicUnit)
    assert(isinstance(iterable['b'], list))
    assert(isinstance(iterable['b'][0], GraphicUnit))
    assert(iterable['b'][0] == GraphicUnit(6))


def test_convert_all_to_unit_tuple_in_dict():
    iterable = {'a': 5, 'b': (6, 7)}
    convert_all_to_unit(iterable, GraphicUnit)
    assert(isinstance(iterable['b'], tuple))
    assert(isinstance(iterable['b'][0], GraphicUnit))
    assert(iterable['b'][0] == GraphicUnit(6))


def test_convert_all_to_unit_dict_in_dict():
    iterable = {'a': 5, 'b': {6: 7}}
    convert_all_to_unit(iterable, GraphicUnit)
    assert(isinstance(iterable['b'], dict))
    assert(isinstance(iterable['b'][6], GraphicUnit))
    assert(iterable['b'][6] == GraphicUnit(7))


def test_convert_all_to_unit_handles_strings_correctly():
    iterable = {'a': 5, 'b': ['abcd', 2]}
    convert_all_to_unit(iterable, GraphicUnit)
    assert(isinstance(iterable['b'][1], GraphicUnit))
    assert(iterable['b'][1] == GraphicUnit(2))
    assert(iterable['b'][0] == 'abcd')
