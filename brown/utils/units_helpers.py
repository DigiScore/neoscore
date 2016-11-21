"""Helper functions related to units.

To be merged later when unit classes are combined into units.py
TODO: Remember to merge me
"""


def convert_contents_to_unit_in_place(working_list, unit_class):
    """Convert all numerical elements in an iterable to a unit.

    Args:
        working_list (list): The list to operate on
        unit_class (type): The unit to convert numerical elements to

    Returns: None
    """
    for i in range(len(working_list)):
        try:
            working_list[i] = unit_class(working_list[i])
        except TypeError:
            continue


def recursively_convert_contents_to_unit_out_of_place(iterable, unit_class):
    """Recursively convert all numbers found in an iterable to a unit out of place.

    This function works in place. Immutable structures (namely tuples) found
    within `iterable` will be replaced. `iterable` itself may not be immutable.

    In dictionaries, *only values* will be converted. Keys will be left as-is.

    Args:
        iterable [set, list, dict]: The iterable to recursive convert
        unit_class (type): The unit to convert numerical elements to

    Returns:
        None

    Raises:
        TypeError: If `iterable` is not an iterable or is immutable
    """
    original_type = type(iterable)
    mutable_iterable = list(iterable)
    recursively_convert_contents_to_unit_in_place(mutable_iterable, unit_class)
    return original_type(mutable_iterable)



def recursively_convert_contents_to_unit_in_place(iterable, unit_class):
    """Recursively convert all numbers found in an iterable to a unit in place.

    This function works in place. Immutable structures (namely tuples) found
    within `iterable` will be replaced. `iterable` itself may not be immutable.

    In dictionaries, *only values* will be converted. Keys will be left as-is.

    Args:
        iterable [list, dict]: The iterable to recursive convert
        unit_class (type): The unit to convert numerical elements to

    Returns:
        None

    Raises:
        TypeError: If `iterable` is not an iterable or is immutable
    """
    if isinstance(iterable, dict):
        for key, value in iterable.items():
            if unit_class._is_acceptable_type(value):
                iterable[key] = unit_class(value)
            elif isinstance(value, (list, dict)):
                recursively_convert_contents_to_unit_in_place(iterable[key], unit_class)
            else:
                try:
                    iterable[key] = recursively_convert_contents_to_unit_out_of_place(iterable[key], unit_class)
                except TypeError:
                    continue
    elif isinstance(iterable, list):
        for i in range(len(iterable)):
            if unit_class._is_acceptable_type(iterable[i]):
                iterable[i] = unit_class(iterable[i])
            elif isinstance(iterable[i], (list, dict)):
                recursively_convert_contents_to_unit_in_place(iterable[i], unit_class)
            else:
                try:
                    iterable[i] = recursively_convert_contents_to_unit_out_of_place(iterable[i], unit_class)
                except TypeError:
                    continue
    else:
        raise TypeError
