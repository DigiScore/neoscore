#!/usr/bin/env python

import abc


class BaseUnit(metaclass=abc.ABCMeta):
    """
    An abstract base class for units which handle typical operators
    and keep track of what type of unit they are.

    Subclasses may implement conversions to other units
    """
    @abc.abstractmethod
    def __init__(self, value):
        """
        Args:
            value (Any):
        """
        self.value = value

    @abc.abstractproperty
    def _allow_operators_with_numbers(self):
        """
        bool: Whether or not this unit will allow operators
        (ie. addition, multiplication) with numbers
        """
        raise NotImplementedError

    @abc.abstractproperty
    def _return_number_when_using_operator_with_number(self):
        """
        bool: When this unit is used in an operator with a number,
            determines whether or not the returning value
            will be a number of a unit
        """
        raise NotImplementedError

    # Operators --------------------------------------------------------------------------------------------------------

    def __add__(self, other):
        if isinstance(other, type(self)):
            # return type(self).__name__(self.value + other.value)
            return self.__class__(self.value + other.value)
        elif self._allow_operators_with_numbers and (isinstance(other, int) or isinstance(other, float)):
            value = self.value + other
            if self._return_number_when_using_operator_with_number:
                return value
            else:
                return self.__class__(value)
        else:
            # raise TypeError('Cannot add %s and %s' % type(self).__name__, type(other).__name__)
            raise TypeError('Cannot add {0} and {1}'.format(type(self).__name__, type(other).__name__))

    def __sub__(self, other):
        if isinstance(other, type(self)):
            return self.__class__(self.value - other.value)
        elif self._allow_operators_with_numbers and (isinstance(other, int) or isinstance(other, float)):
            value = self.value - other
            if self._return_number_when_using_operator_with_number:
                return value
            else:
                return self.__class__(value)
        else:
            raise TypeError('Cannot subtract {0} and {1}'.format(type(self).__name__, type(other).__name__))

    def __mul__(self, other):
        if isinstance(other, type(self)):
            return self.__class__(self.value * other.value)
        elif self._allow_operators_with_numbers and (isinstance(other, int) or isinstance(other, float)):
            value = self.value * other
            if self._return_number_when_using_operator_with_number:
                return value
            else:
                return self.__class__(value)
        else:
            raise TypeError('Cannot multiply {0} and {1}'.format(type(self).__name__, type(other).__name__))

    def __truediv__(self, other):
        if isinstance(other, type(self)):
            return self.__class__(self.value / other.value)
        elif self._allow_operators_with_numbers and (isinstance(other, int) or isinstance(other, float)):
            value = self.value / other
            if self._return_number_when_using_operator_with_number:
                return value
            else:
                return self.__class__(value)
        else:
            raise TypeError('Cannot divide {0} and {1}'.format(type(self).__name__, type(other).__name__))

    def __neg__(self):
        return self.__class__(self.value * -1)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.value == other.value
        elif self._allow_operators_with_numbers and (isinstance(other, int) or isinstance(other, float)):
            return self.value == other
        else:
            # raise TypeError('Cannot compare {0} and {1}'.format(type(self).__name__, type(other).__name__))
            return False

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return self.value != other.value
        elif self._allow_operators_with_numbers and (isinstance(other, int) or isinstance(other, float)):
            return self.value != other
        else:
            raise TypeError('Cannot compare {0} and {1}'.format(type(self).__name__, type(other).__name__))

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.value < other.value
        elif self._allow_operators_with_numbers and (isinstance(other, int) or isinstance(other, float)):
            return self.value < other
        else:
            raise TypeError('Cannot compare {0} and {1}'.format(type(self).__name__, type(other).__name__))

    def __le__(self, other):
        if isinstance(other, type(self)):
            return self.value <= other.value
        elif self._allow_operators_with_numbers and (isinstance(other, int) or isinstance(other, float)):
            return self.value <= other
        else:
            raise TypeError('Cannot compare {0} and {1}'.format(type(self).__name__, type(other).__name__))

    def __gt__(self, other):
        if isinstance(other, type(self)):
            return self.value > other.value
        elif self._allow_operators_with_numbers and (isinstance(other, int) or isinstance(other, float)):
            return self.value > other
        else:
            raise TypeError('Cannot compare {0} and {1}'.format(type(self).__name__, type(other).__name__))

    def __ge__(self, other):
        if isinstance(other, type(self)):
            return self.value >= other.value
        elif self._allow_operators_with_numbers and (isinstance(other, int) or isinstance(other, float)):
            return self.value >= other
        else:
            raise TypeError('Cannot compare {0} and {1}'.format(type(self).__name__, type(other).__name__))
