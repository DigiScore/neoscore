#!/usr/bin/env python

import fractions
import re


def float_to_rhythm(rhythm):
    """
    Takes an input rhythm as a float between 0 and 1, returns the nearest easily notated rhythm in string format
    Rounds the input rhythm into musically convenient slots and prefers more common rhythms
        (dots and double dots are made less common)
    :param rhythm: float
    :return: str
    """
    rhythm = float(rhythm)
    better_list = [(0.03125, '32'), (0.0625, '16'), (0.125, '8'),
                   (0.5, '4'), (0.75, '2.'), (1.0, '1')]
    worse_list = [(0.09375, '16.'), (0.1875, '8.'), (0.21875, '8..'), (0.4375, '4..'),
                  (0.875, '2..'), (1.5, '1.'), (1.75, '1..')]

    def smallest_dist(test_list, test_point):
        # Simple private function for finding the smallest distance available from a point to a given list
        # Used to determine if worse_list should be used in the outer scope
        smallest_found = 1000
        for point in test_list:
            test_dist = abs(point - test_point)
            if test_dist < smallest_found:
                smallest_found = test_dist
        return smallest_found
    # Find the error if we were to use the better_list
    better_error = smallest_dist([i[0] for i in better_list], rhythm)
    # If the better error is too large (over 0.1), see if we can get a significantly closer value using worse_list
    if better_error > 0.1:
        worse_error = smallest_dist([i[0] for i in worse_list], rhythm)
        if worse_error < better_error + 0.035:
            rounded_number = min([i[0] for i in worse_list], key=lambda x: abs(x - rhythm))
            out_index = [y[0] for y in worse_list].index(rounded_number)
            return worse_list[out_index][1]

    # Otherwise just go with better_list
    rounded_number = min([i[0] for i in better_list], key=lambda x: abs(x - rhythm))
    out_index = [y[0] for y in better_list].index(rounded_number)
    return better_list[out_index][1]


def approximate_rhythm_dist(rhythm):
    """
    Takes a number between 0 and 1 and approximates it graphical space in mm.
    Assumes that a whole note occupies about 6mm
    :param rhythm: float
    :return: float
    """
    return rhythm * 6.0


def rhythm_string_to_base_and_dots(rhythm_string):
    """
    Take a rhythm_string and split it into base value and a number of dots using re.

    The re pattern is ``'\A(\d+)(.+)\Z'``. In plain English this means the string must begin with digits and end with
    any number of dots (or no dots). Non-matching values will raise ValueError.

    Args:
        rhythm_string (str):

    Returns: (int, int) representing (base_value, dot_count)

    Raises: ValueError if an invalid rhythm_string is passed

    """
    # TODO: this isn't really mistake-proof right now, for example rhythm_string = '1f6..' returns (1, 4)
    # TODO: What about breves? How will they be represented?
    match = re.match('\A(\d+)(.*)\Z', rhythm_string)
    if not match:
        raise ValueError('rhythm_string value of %s is invalid. A valid rhythm_string must begin with numbers and end '
                          'with any number of dots (or no dots). For example, \'16\' or \'2..\'' % rhythm_string)

    return int(match.group(1)), len(match.group(2))


def rhythm_string_to_float(rhythm_string, tuplet_ratio=None):
    """
    Takes a lilypond-style rhythm string and converts it into a float value where 1 is a whole note,
        0.5 is a half note, 16. is a dotted half note, etc.
    Args:
        rhythm_string (str):
        tuplet_ratio (fractions.Fraction or tuple or None):

    Returns: float
    """
    if not isinstance(rhythm_string, str):
        raise TypeError('rhythm_string in rhythm_tools.rhythm_string_to_float() must be a str')

    if tuplet_ratio is None or isinstance(tuplet_ratio, fractions.Fraction):
            pass
    elif isinstance(tuplet_ratio, tuple):
        tuplet_ratio = fractions.Fraction(*tuplet_ratio)
    else:
        raise TypeError('RhythmicValue.tuplet_ratio must be either None, tuple, or fractions.Fraction')
    # TODO: what about nested tuplets?

    base_value, dot_count = rhythm_string_to_base_and_dots(rhythm_string)

    # Convert base_value to float
    value = 1.0 / float(base_value)

    # Add dots to base value
    dot_value = value
    for i in range(dot_count):
        dot_value /= 2.0
        value += dot_value

    # Modify value to fit the tuplet_ratio
    # Divide value by tuplet_ratio
    if tuplet_ratio is not None:
        value /= tuplet_ratio

    return value

def base_value_and_dots_to_float(base_value, dot_count, tuplet_ratio=None):
    """
    Take a given base value, dot_count, and optional tuplet ratio and convert it to a float where
    Args:
        base_value (int or float):
        dot_count (int):
        tuplet_ratio (fractions.Fraction or tuple or None):

    Returns:

    """
    # This code is taken mostly from rhythm_string_to_float()
    # type-check tuplet_ratio
    if tuplet_ratio is None or isinstance(tuplet_ratio, fractions.Fraction):
            pass
    elif isinstance(tuplet_ratio, tuple):
        tuplet_ratio = fractions.Fraction(*tuplet_ratio)
    else:
        raise TypeError('RhythmicValue.tuplet_ratio must be either None, tuple, or fractions.Fraction')
    # Convert base_value to float
    value = 1.0 / float(base_value)

    # Add dots to base value
    dot_value = value
    for i in range(dot_count):
        dot_value /= 2.0
        value += dot_value

    # Modify value to fit the tuplet_ratio
    # Divide value by tuplet_ratio
    if tuplet_ratio is not None:
        value /= tuplet_ratio

    return value


def rhythm_can_have_flag(rhythmic_value):
    """
    Determine whether a given rhythmic_value can have a flag

    Args:
        rhythmic_value (RhythmicValue):

    Returns: bool - True if the rhythmic value is smaller than a quarter note, False if not
    """
    if rhythmic_value.base_value > 4:
        return True
    else:
        return False
