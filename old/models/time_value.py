#!/usr/bin/env python

class TimeDuration:
    """
    A value measured in milliseconds
    """
    def __init__(self, value):
        try:
            value = float(value)
        except ValueError:
            raise TypeError('value in TimeDuration.__init__() must be a number')
        self.value = value

