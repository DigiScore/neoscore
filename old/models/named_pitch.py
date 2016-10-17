#!/usr/bin/env python
from .tools import pitch_tools
from .accidental import Accidental
from .exceptions import IncompatibleValuesError


class NamedPitch:
    """
    A pitch with an absolute pitch number, and octave, a pitch letter name, an name

    Adjustments to any one of the four properties of this class will trigger adjustments to all others accordingly
    such that this object should always form a logical description of an actual note pitch
    """
    def __init__(self, pitch_number=None, letter=None, accidental=None, octave=None, show_natural=True):
        """
        Initializes the NamedPitch from the given list of values passed.

        There are many ways a complete description of a NamedPitch may be initialized. For example,
        from just an absolute pitch_number and an name the letter name and octave can be inferred;
        from a letter name, name, and octave an absolute pitch_number can be found. This initialization
        will raise a ValueError if it is impossible to infer information about the NamedPitch from the given
        input arguments.

        Args:
            pitch_number (int): Absolute pitch number where 0 refers to Middle C
            letter (char): A-G letter name of the pitch
            accidental (str or Accidental or None): Name of the name to be used.
            octave (int): Absolute octave number where 0 refers tot he octave spanning Middle C to its above B

        Raises:
            ValueError if it is impossible to infer the complete NamedPitch from the given list of inputs
            ValueError if the given inputs are contradictory (e.g. if pitch_number is passed as 0 and letter
                is passed as G, it is not possible for a G to occupy that pitch without a quintuple-sharp...)

        """
        # Count the number of passed parameters
        parameter_count = 0
        if pitch_number is not None:
            parameter_count += 1
        if letter is not None:
            parameter_count += 1
        if accidental is not None:
            parameter_count += 1
        if octave is not None:
            parameter_count += 1
        # If we have less than 3 parameters passed
        if parameter_count < 3:
            if pitch_number is not None:
                # Check the few cases where it is still possible to initialize
                if letter is not None:
                    # With a pitch_number and letter, this is possible, initialize
                    self.pitch_number = pitch_number
                    self.letter = letter
                    self.accidental = pitch_tools.find_accidental_for_pitch_num_and_letter(self.pitch_number, self.letter)
                    self.octave = pitch_tools.find_octave(self.pitch_number, self.letter)
                    return
                if accidental is not None:
                    # With a pitch_number and name, this is possible, initialize
                    self.pitch_number = pitch_number
                    self.accidental = accidental
                    self.letter = pitch_tools.find_letter_of_pitch_num_and_accidental(self.pitch_number, self.accidental)
                    self.octave = pitch_tools.find_octave(self.pitch_number, self.letter)
                    return
            else:
                # Otherwise, raise ValueError - it isn't possible to infer this NamedPitch
                raise TypeError('With the given parameters there is not enough information to construct a NamedPitch')

        # If we have exactly 3 parameters passed it will always be possible to initialize
        # (unless the parameters are contradictory)
        if parameter_count == 3:
            if pitch_number is None:
                # With a letter, accidental, and octave it is impossible to be contradictory - no need to validate
                # Pass parameters to instance properties
                self.letter = letter
                self.accidental = accidental
                self.octave = octave
                # Find pitch_num
                self.pitch_number = pitch_tools.find_pitch_in_octave(
                        pitch_tools.find_pitch_class_of_letter_and_accidental(self.letter, self.accidental),
                        self.octave)
                return
            if octave is None:
                # With a pitch_number, letter, and name it is impossible to be contradictory - no need to validate
                # Pass parameters to instance properties
                self.pitch_number = pitch_number
                self.letter = letter
                self.accidental = accidental
                # Find octave
                self.octave = pitch_tools.find_octave(self.pitch_number, self.letter)
                return
            if letter is None:
                # Assure that octave and pitch_number are consistent
                # Pass parameters to instance properties
                self.pitch_number = pitch_number
                self.accidental = accidental
                # Find letter
                self.letter = pitch_tools.find_letter_of_pitch_num_and_accidental(self.pitch_number, self.accidental)
                if pitch_tools.find_octave(self.pitch_number, self.letter) != octave:
                    raise IncompatibleValuesError
                self.octave = octave
                return
            if accidental is None:
                # Ensure that pitch_number and letter are within a double sharp or double flat of each other
                pitch_distance = abs(pitch_tools.find_pitch_class(pitch_number) -
                                     pitch_tools.find_natural_pitch_class_of_letter(letter))
                if pitch_distance > 2:
                    raise IncompatibleValuesError('A pitch_number of {0} and a letter name of {1} are incompatible'
                                                  .format(str(pitch_number), letter))
                # Pass parameters to instance properties
                self.pitch_number = pitch_number
                self.letter = letter
                if pitch_tools.find_octave(self.pitch_number, self.pitch_number) != octave:
                    raise IncompatibleValuesError
                self.octave = octave
                # Find name
                self.accidental = pitch_tools.find_accidental_for_pitch_num_and_letter(pitch_number, letter)
                return

        # If we have all four parameters available, validate the given parameters
        if pitch_tools.find_octave(pitch_number, letter) != octave:
            raise IncompatibleValuesError('pitch_number of {0} with letter {1} and octave {2} contradict each other'
                                          .format(str(pitch_number), letter, str(octave)))
        pitch_distance = abs(pitch_tools.find_pitch_class(pitch_number) -
                             pitch_tools.find_natural_pitch_class_of_letter(letter))
        if pitch_distance > 2:
            raise IncompatibleValuesError('A pitch_number of {0} and a letter name of {1} are incompatible'
                                          .format(str(pitch_number), letter))
        if pitch_tools.find_pitch_in_octave(
                pitch_tools.find_pitch_class_of_letter_and_accidental(letter, accidental),
                octave) != pitch_number:
            raise IncompatibleValuesError(
                'The given letter, name, and octave do not match the given pitch_number of {0}'
                .format(str(pitch_number)))
        # If everything is consistent, pass the parameters to instance properties
        self.pitch_number = pitch_number
        self.letter = letter
        self.accidental = accidental
        self.octave = octave
        return

    @property
    def pitch_class(self):
        """int: Calculate the 0-11 pitch class of this NamedPitch (read-only)"""
        return pitch_tools.find_pitch_class(self.pitch_number)

    @property
    def pitch_number(self):
        """int: The number corresponding to this pitch where 0 is middle C"""
        return self._pitch_number

    @pitch_number.setter
    def pitch_number(self, number):
        self._pitch_number = number

    @property
    def octave(self):
        """int: The octave of this named_pitch where 0 is the octave spanning middle C to its higher B.
        Changing this value will *automatically* adjust self.pitch_number"""
        return self._octave

    @octave.setter
    def octave(self, new_octave):
        if not isinstance(new_octave, int):
            raise TypeError('NamedPitch.octave must be an int')
        self._octave = new_octave
        if hasattr(self, '_pitch_number'):
            self.pitch_number = pitch_tools.find_pitch_in_octave(self.pitch_number, new_octave)

    @property
    def letter(self):
        """char: The c-b letter name of the pitch. May be capitalized or not."""
        return self._letter

    @letter.setter
    def letter(self, name):
        name = name.lower()
        if name not in ['c', 'd', 'e', 'f', 'g', 'a', 'b']:
            raise ValueError("NamedPitch.letter must be a char between 'a' and 'g'")
        self._letter = name

    @property
    def accidental(self):
        """Accidental: """
        return self._accidental

    @accidental.setter
    def accidental(self, new_accidental):
        if isinstance(new_accidental, Accidental):
            # If the name is actually any name object, attach it directly to self._accidental
            self._accidental = new_accidental
        else:
            # Otherwise pass new_accidental as the value for a newly created Accidental object to be attached
            self._accidental = Accidental(new_accidental)

    def transpose(self, interval, direction):
        """
        Transposes this object by a given Interval in a given direction

        Args:
            interval (Interval): [Maybe allow interval to also be a str representation of an interval?]
            direction (int): -1 for down, 1 for up

        Returns: None
        """
        # TODO: Build me
        pass
