"""Helper functions related to units.

To be merged later when unit classes are combined into units.py
TODO: Remember to merge me
"""


def convert_contents_to_unit_in_place(working_list, unit):
    """Convert all numerical elements in an iterable to a unit.

    Args:
        working_list (list): The list to operate on
        unit (type): The unit to convert numerical elements to

    Returns: None
    """
    for i in range(len(working_list)):
        try:
            working_list[i] = unit(working_list[i])
        except TypeError:
            continue


def _call_on_immutable(iterable, unit):
    """Recursively convert all numbers in an immutable iterable.

    This is a helper function for convert_all_to_unit

    Args:
        iterable [tuple]: The iterable to recursive convert
        unit (type): The unit to convert numerical elements to

    Returns:
        An iterable the same type of the input.
        (set --> set, tuple --> tuple, etc.)
    """
    original_type = type(iterable)
    mutable_iterable = list(iterable)
    convert_all_to_unit(mutable_iterable, unit)
    return original_type(mutable_iterable)



def convert_all_to_unit(iterable, unit):
    """Recursively convert all numbers found in an iterable to a unit in place.

    This function works in place. Immutable structures (namely tuples) found
    within `iterable` will be replaced. `iterable` itself may not be immutable.

    In dictionaries, *only values* will be converted. Keys will be left as-is.

    Args:
        iterable [list, dict]: The iterable to recursive convert
        unit (type): The unit to convert numerical elements to

    Returns:
        None

    Raises:
        TypeError: If `iterable` is not an iterable or is immutable
    """
    if isinstance(iterable, dict):
        for key, value in iterable.items():
            if unit._is_acceptable_type(value):
                iterable[key] = unit(value)
            elif isinstance(value, (list, dict)):
                convert_all_to_unit(iterable[key], unit)
            elif isinstance(value, (tuple, set)):
                try:
                    iterable[key] = _call_on_immutable(iterable[key], unit)
                except TypeError:
                    continue
            else:
                # Nothing left to do at this item, continue
                continue
    elif isinstance(iterable, list):
        for i in range(len(iterable)):
            if unit._is_acceptable_type(iterable[i]):
                iterable[i] = unit(iterable[i])
            elif isinstance(iterable[i], (list, dict)):
                convert_all_to_unit(iterable[i], unit)
            elif isinstance(iterable[i], (tuple, set)):
                try:
                    iterable[i] = _call_on_immutable(iterable[i], unit)
                except TypeError:
                    continue
            else:
                # Nothing left to do at this item, continue
                continue
    else:
        raise TypeError
