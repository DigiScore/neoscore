s#!/usr/bin/env python

from .point_unit import PointUnit


class Paper:
    """
    A container for various properties for paper types, including size and margins.

    Is not a GraphicObject - real pages with graphical contents must be created through ``page.Page`` objects
        (which contain a reference to a Paper object)
    """

    def __init__(self, width, height, margin_left, margin_right, margin_top, margin_bottom):
        """
        Args:
            width (int, float, or PointUnit):
            height (int, float, or PointUnit):
            margin_left (int, float, or PointUnit):
            margin_right (int, float, or PointUnit):
            margin_top (int, float, or PointUnit):
            margin_bottom (int, float, or PointUnit):
        """
        self.width = width
        self.height = height
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.margin_top = margin_top
        self.margin_bottom = margin_bottom

    @classmethod
    def from_default_paper_type(cls, paper_type):
        """
        Construct and return a Paper object based on a string name of a common paper type.

        Supported paper_type values include: ``'letter'``, ``'a4'``

        Args:
            paper_type (str):

        Returns: Paper
        """
        # Note that paper_type values are case-insensitive
        if paper_type.lower() == 'letter':
            # In inches, 8.5 x 11 size with 1 inch margins on all sides
            return Paper(612, 792, 72, 72, 72, 72)
        if paper_type.lower() == 'a4':
            # In millimeters, 210 x 297 with 2.5 cm margins on all sides.
            # (Standard Postscript roundings are used for conversion to 72-dpi points)
            return Paper(595, 842, 71, 71, 71, 71)
        # ...
        else:
            raise ValueError

    # TODO: Implement gutter-style margins

    @property
    def margin_left(self):
        """PointUnit: Size of the paper's left margin"""
        return self._margin_left

    @margin_left.setter
    def margin_left(self, new_value):
        self._margin_left = PointUnit(new_value)

    @property
    def margin_right(self):
        """PointUnit: Size of the paper's right margin"""
        return self._margin_right

    @margin_right.setter
    def margin_right(self, new_value):
        self._margin_right = PointUnit(new_value)

    @property
    def margin_top(self):
        """PointUnit: Size of the paper's top margin"""
        return self._margin_top

    @margin_top.setter
    def margin_top(self, new_value):
        self._margin_top = PointUnit(new_value)

    @property
    def margin_bottom(self):
        """PointUnit: Size of the paper's bottom margin"""
        return self._margin_bottom

    @margin_bottom.setter
    def margin_bottom(self, new_value):
        self._margin_bottom = PointUnit(new_value)

    @property
    def width(self):
        """PointUnit: The width of the paper"""
        return self._width

    @width.setter
    def width(self, new_value):
        self._width = PointUnit(new_value)

    @property
    def height(self):
        """PointUnit: The width of the paper"""
        return self._height

    @height.setter
    def height(self, new_value):
        self._height = PointUnit(new_value)
