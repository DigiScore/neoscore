#!/usr/bin/env python
import fractions
from .tools import rhythm_tools
import re


class RhythmicValue:
    """
    A class containing a rhythmic value for use in NoteColumn objects or otherwise
    """
    def __init__(self, rhythm_string, tuplet_ratio=None):
        """
        Args:
            rhythm_string (str): rhythmic value of the note in Lilypond vocabulary
                '1' - Whole Note
                '2' - Half Note
                '4' - Quarter Note
                '16.' - Dotted 16th Note
                etc.
            tuplet_ratio (tuple, fractions.Fraction, or None):
        """
        self.base_value, self.dot_count = rhythm_tools.rhythm_string_to_base_and_dots(rhythm_string)
        self.tuplet_ratio = tuplet_ratio

    @property
    def base_value(self):
        """(int or float): The basic rhythmic value independent of dots and tuplet ratios.
        Numbered in lily-pond style where '1' - Whole Note, '2' - Half Note, '4' - Quarter Note, etc.
        For a breve value use 0.5"""
        return self._base_value
    
    @base_value.setter
    def base_value(self, new_value):
        if not isinstance(new_value, int) and not isinstance(new_value, float):
            raise TypeError('RhythmicValue.base_value must be an int or float')
        # Could possibly also check that base_value is a power of 2
        self._base_value = new_value

    @property
    def dot_count(self):
        return self._dot_count

    @dot_count.setter
    def dot_count(self, new_dot_count):
        if not isinstance(new_dot_count, int):
            try:
                new_dot_count = int(new_dot_count)
            except ValueError:
                raise TypeError('RhythmicValue.dot_count must be an int')
        self._dot_count = new_dot_count

    @property
    def tuplet_ratio(self):
        return self._tuplet_ratio
    
    @tuplet_ratio.setter
    def tuplet_ratio(self, new_ratio):
        if new_ratio is None:
            new_ratio = fractions.Fraction(1, 1)
        elif isinstance(new_ratio, tuple):
            new_ratio = fractions.Fraction(*new_ratio)
        elif isinstance(new_ratio, fractions.Fraction):
            pass
        else:
            raise TypeError('RhythmicValue.tuplet_ratio must be either None, tuple, or fractions.Fraction')
        self._tuplet_ratio = new_ratio

    @property
    def float_value(self):
        return rhythm_tools.base_value_and_dots_to_float(self.base_value, self.dot_count, self.tuplet_ratio)
