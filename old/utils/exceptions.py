#!/usr/bin/env python
"""
Custom exceptions shared by various modules
"""


class IncompatibleValuesError(Exception):
    """
    Is raised when an incompatible set of values is used in manipulating pitch data
    """
    pass


class PageNotInDocumentError(Exception):
    """
    Is raised when a Document tries to access a page not contained in its page_list
    """
    pass


class NoPageAtCoordinateError(Exception):
    """
    Is raised when a Document tries to find a page under a given coordinate,
    but there is no page under that coordinate.
    """
    pass


class PointOutsideSectionError(Exception):
    """
    Is raised when a Flowable tries to identify which FlowableSection contains a given coordinate.
    """
    pass
