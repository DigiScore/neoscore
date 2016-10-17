#!/usr/bin/env python

from ..accidental import Accidental
from ..exceptions import IncompatibleValuesError


def find_pitch_class(pitch):
    """
    Finds the 0-11 pitch class of any pitch
    :param pitch: int
    :return:int pitch class of 0-11
    """
    if not isinstance(pitch, int):
        pitch = int(pitch)
    if pitch <= 0:
        direction = 1
    else:
        direction = -1
    while not (0 <= pitch <= 11):
        pitch += direction * 12
    return pitch


def find_octave(pitch_num, letter=None):
    """
    Finds the octave of a given pitch_num where 0 is the octave spanning middle C to its above C

    Accepts an optional letter argument which is used to ensure that cases such as Cb and B# actually
    result in the appropriate octave. If letter is not given, the enharmonic default value will be used
    for edge cases.

    Args:
        pitch_num (int): absolute pitch number to find the octave of
        letter (str): Optional (but highly recommended) letter name of the pitch_num

    Returns: int
    """
    # If the letter is an edge case, adjust pitch_num to the nearest natural version of letter and test that instead
    if letter == 'c' or letter == 'b':
        natural_pitch_class = find_natural_pitch_class_of_letter(letter)
        pitch_num = find_nearest_version_of_pitch_class(natural_pitch_class, pitch_num)
    return divmod(pitch_num, 12)[0]


def find_pitch_in_octave(pitch_number, octave):
    """
    Takes a given ``pitch_number`` and finds that number's 0-11 pitch-class equivalent within a given ``octave``
    Args:
        pitch_number (int):
        octave (int):

    Returns (int):
    """
    # Find the 0-11 pitch class of pitch_number
    pitch_class = find_pitch_class(pitch_number)
    return pitch_class + (octave * 12)


def find_nearest_version_of_pitch_class(pitch_class, pitch_num):
    """
    Finds the nearest version of a pitch class relative to a given pitch_num

    Note: If the distance between pitch_class and pitch_num is a tritone, the nearest version will default downward
    Args:
        pitch_class (int):
        pitch_num (int):

    Returns: int
    """
    # Convert pitch_class to a pitch class if outside the range of 0-11
    if not (0 <= pitch_class <= 11):
        pitch_class = find_pitch_class(pitch_class)
    pitch_class_difference = find_pitch_class(pitch_num) - pitch_class
    # Adjust pitch_class_difference to wrap from +- 11 to 0
    if pitch_class_difference > 6:
        pitch_class_difference -= 12
    elif pitch_class_difference < -6:
        pitch_class_difference += 12
    return pitch_num - pitch_class_difference


def find_letter_distance(named_pitch_1, named_pitch_2):
    """
    Takes two NamedPitch objects and finds the letter distance from the first to the second

    Args:
        named_pitch_1 (NamedPitch):
        named_pitch_2 (NamedPitch):

    Returns: int
    """
    # Find the direction of distance
    if named_pitch_1.pitch_number < named_pitch_2.pitch_number:
        direction = 1
    else:
        direction = -1
    # Set up a letter-to-int dictionary which will allow convenient comparison of letter values
    letter_int_dict = {'c': 1, 'd': 2, 'e': 3, 'f': 4, 'g': 5, 'a': 6, 'b': 7}
    return ((letter_int_dict[named_pitch_2.letter] + (7 * named_pitch_2.octave)) -
            (letter_int_dict[named_pitch_1.letter] + (7 * named_pitch_1.octave)))


def get_pitch_string(pitch_num, mode='sharp'):
    """
    Takes a given pitch_num and returns a lilypond-ready pitch string
    (it's possible to have a higher-up algorithm analyze a passage and pass mixed modes to this within a passage)
    :param pitch_num: int
    :param mode: str 'sharp' or 'flat' (will default to 'flat' if invalid)
    :return: str
    """
    # Middle C is index 0, which should be represented in a lilypond string as c'
    # Adjust pitch num by adding 12 to reconcile the difference for easy divmod manipulation later
    adjusted_pitch_num = pitch_num + 12

    sharp_pitch_dict = {0: 'c', 1: 'cs', 2: 'd', 3: 'ds', 4: 'e', 5: 'f',
                        6: 'fs', 7: 'g', 8: 'gs', 9: 'a', 10: 'as', 11: 'b'}
    flat_pitch_dict = {0: 'c', 1: 'df', 2: 'd', 3: 'ef', 4: 'e', 5: 'f',
                       6: 'gf', 7: 'g', 8: 'af', 9: 'a', 10: 'bf', 11: 'b'}
    if mode == 'sharp':
        base_string = sharp_pitch_dict[find_pitch_class(adjusted_pitch_num)]
    else:
        base_string = flat_pitch_dict[find_pitch_class(adjusted_pitch_num)]

    if adjusted_pitch_num > 0:
        ticks_num = divmod(adjusted_pitch_num, 12)[0]
    else:
        ticks_num = divmod(adjusted_pitch_num, -12)[0]
    if adjusted_pitch_num > 0:
        tick_string = "'" * ticks_num
    else:
        tick_string = "," * ticks_num
    out_string = base_string + tick_string
    return out_string


def find_accidental_for_pitch_num_and_letter(pitch_num, letter):
    """
    Takes a pitch_num and letter and determines the name needed to make the letter fit in pitch_num

    Args:
        pitch_num (int): Where 0 is Middle C
        letter (char): A-G

    Returns: Accidental, or None if it would require more than a double flat or double sharp
    """
    # TODO: shorten function name
    natural_pitch_num = find_natural_pitch_num_of_letter(letter, find_octave(pitch_num, letter))
    pitch_difference = pitch_num - natural_pitch_num
    if abs(pitch_difference) > 2:
        # If this would require more than a double flat or double sharp, return None
        raise IncompatibleValuesError('pitch_num of {0} and letter of {1} are incompatible.'
                                      .format(str(pitch_num), letter))

    accidental_dict = {-2: 'double flat', -1: 'flat', 0: 'natural', 1: 'sharp', 2: 'double sharp'}
    return Accidental(accidental_dict[pitch_difference])


def find_pitch_class_of_letter_and_accidental(letter, accidental):
    """
    Takes a letter and name and finds the appropriate pitch class

    Args:
        letter (str):
        accidental (str or Accidental):

    Returns: int

    """
    if not isinstance(letter, str):
        raise TypeError('letter must be a str')
    if not isinstance(accidental, Accidental):
        accidental = Accidental(accidental)
    return find_natural_pitch_class_of_letter(letter) + accidental.pitch_offset


def find_natural_pitch_num_of_letter(letter, octave):
    """
    Takes a given letter and octave and finds the natural pitch_number of that letter
    Args:
        letter (chr): A-G
        octave (int):

    Returns: int
    """
    if not isinstance(letter, str):
        raise TypeError('letter must be of type str')
    letter = letter.lower()
    diatonic_dict = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}
    try:
        natural_pitch_class = diatonic_dict[letter]
    except KeyError:
        # Is this bad practice?
        raise ValueError('letter must be between A and G')

    return find_pitch_in_octave(natural_pitch_class, octave)


def find_natural_pitch_class_of_letter(letter):
    """
    Takes a given letter and finds the natural 0-11 pitch class of that letter
    Args:
        letter (chr): A-G

    Returns: int
    """
    if not isinstance(letter, str):
        raise TypeError('letter must be of type str')
    letter = letter.lower()
    diatonic_dict = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}
    try:
        return diatonic_dict[letter]
    except KeyError:
        raise ValueError('letter must be between A and G')


def find_letter_of_natural_pitch_num(pitch_num):
    """
    Take a given pitch_num (or pitch class) and, if the pitch class is a natural pitch, find the letter

    If the pitch class of pitch_num is not a natural (white key) pitch, such as ``1``, return None

    Args:
        pitch_num (int): Where 0 is Middle C. May also be a 0-11 pitch class

    Returns: str or None
    """
    pitch_num = find_pitch_class(pitch_num)
    letter_dict = {0: 'c', 2: 'd', 4: 'e', 5: 'f', 7: 'g', 9: 'a', 11: 'b'}
    try:
        return letter_dict[pitch_num]
    except KeyError:
        return None


def find_letter_of_pitch_num_and_accidental(pitch_num, accidental):
    """
    Takes a given name and pitch_num and finds the needed letter to satisfy the pitch.

    Args:
        pitch_num (int): Where 0 is Middle C
        accidental (Accidental or str representation of an Accidental):

    Returns: str
    """
    if not isinstance(accidental, Accidental):
        accidental = Accidental(accidental)
    accidental_offset = accidental.pitch_offset
    # Invert the name offset to the find the natural version of the pitch
    natural_pitch_num = pitch_num - accidental_offset
    return find_letter_of_natural_pitch_num(natural_pitch_num)


def extend_pitches_through_range(pitch_class_list, lowest, highest):
    """
    Takes a list of pitch classes (int's between 0 and 11) and transposes and extends it through the window given
    :param pitch_class_list: list of int's
    :param min: int
    :param max: int
    :return: extended list
    """
    assert isinstance(pitch_class_list, list)
    full_range = range(lowest, highest)
    return_list = []
    for pitch in full_range:
        if find_pitch_class(pitch) in pitch_class_list:
            return_list.append(pitch)
    return return_list


def find_active_accidental_in_staff(staff, test_x_pos, test_letter, test_octave, test_distance=None):
    """

    Finds the current accidental state in a staff at a given horizontal location, pitch letter name, and octave.

    Primarily useful for determining if an accidental needs to be drawn at a given location in a NoteColumn

    Args:
        staff (Staff):
        test_x_pos (StaffUnit or float or int):
        test_letter (str): c - b letter name of the pitch to test
        test_octave (int): octave of the pitch to test
        test_distance: The distance before the test_x_pos for which the function should test.
            None will test everything before test_x_pos.

    Returns: Accidental or None

    """
    # Do potentially cyclic imports at this level to avoid ImportErrors. A little messy and maybe slow.
    # TODO: Rework to pass just a staff unit position instead of letter and octave
    from ..note_column import NoteColumn
    # Sort staff.contents by horizontal position
    staff_contents = sorted(staff.contents, key=lambda item: item.x_pos)
    comparison_accidental = None
    # Iterate through staff_contents, modifying the state with each item as necessary
    # Break once we reach or go past position
    for item in staff_contents:
        # If we've reached or passed the test_x_pos, break
        if item.x_pos >= test_x_pos:
            break
        if test_distance is not None:
            # continue if we are not within the specified test_distance before test_x_pos
            if item.x_pos < test_x_pos - test_distance:
                continue
        # If this is a Notecolumn, test for notes
        if isinstance(item, NoteColumn):
            # Loop through any items in Notecolumn.contents, and compare any accidentals
            for notehead in item.contents:
                if (hasattr(notehead, 'named_pitch') and
                            notehead.named_pitch.letter == test_letter and
                            notehead.named_pitch.octave == test_octave):
                    # If the notehead has a pitch that is the same letter and octave as pitch_letter and test_octave,
                    # Update comparison_accidental
                    comparison_accidental = notehead.named_pitch.accidental

    return comparison_accidental


def find_accidentals_of_letter_in_staff(staff, test_x_pos, test_letter, test_distance=None):
    """
    At a given horizontal position in a staff, return a list of all active accidentals in all octaves of a test_letter

    Useful for determining if cautionary accidentals are needed

    Args:
        staff (Staff):
        test_x_pos (float or int):
        test_letter (str):
        test_distance (float or int or None): The distance before the test_x_pos for which the function should test.
            None will test everything before test_x_pos.

    Returns: list of Accidental objects

    """
    # Do potentially cyclic imports at this level to avoid ImportErrors. A little messy and maybe slow.
    from ..note_column import NoteColumn
    from ..accidental import Accidental
    # Sort staff.contents by horizontal position
    staff_contents = sorted(staff.contents, key=lambda item: item.x_pos)
    accidental_list = []
    # TODO: build me
