#!/usr/bin/env python

from PySide.QtGui import QGraphicsRectItem

from .graphic_object import GraphicObject
from .paper import Paper
from .point_unit import PointUnit


class Page(GraphicObject):
    """
    A page placed within a QGraphicsScene
    """
    def __init__(self, document, paper, document_page_number, display_page_number='automatic'):
        """
        This method should only be called by a Document. To add a page to a Document, use on of the many dedicated
            methods for this.

        Args:
            document (Document): The document to which this Page belongs
            paper (Paper or str): str values must be a valid argument to ``Paper.from_default_paper_type()``
            document_page_number (int): The document-level page number.
            display_page_number (int or 'automatic'): The display page number.
                If 'automatic', this will be the same as document_page_number.
        """
        self.paper = paper
        self.document_page_number = document_page_number
        self.display_page_number = display_page_number
        self.document = document

        # Register self in document.page_list
        GraphicObject.__init__(self, None, document.scene,
                               document.x_of_document_page_number(self.document_page_number), 0)

    @property
    def paper(self):
        """Paper: The Paper object which defines this Page object's dimensions and margins"""
        return self._paper

    @paper.setter
    def paper(self, new_value):
        if isinstance(new_value, str):
            self._paper =  Paper.from_default_paper_type(new_value)
        elif isinstance(new_value, Paper):
            self._paper = new_value
        else:
            raise TypeError

    @property
    def document_page_number(self):
        """int: The document-level page number"""
        return self._document_page_number

    @document_page_number.setter
    def document_page_number(self, new_value):
        if not isinstance(new_value, int):
            raise TypeError
        self._document_page_number = new_value

    @property
    def display_page_number(self):
        """int: The display page number. If set to 'automatic' assign to self.document_page_number."""
        return self._display_page_number

    @display_page_number.setter
    def display_page_number(self, new_value):
        if new_value == 'automatic':
            self._display_page_number = self.document_page_number
        elif isinstance(new_value, int):
            self._display_page_number = new_value
        else:
            raise TypeError

    @property
    def width(self):
        """PointUnit: The width of the page. This is a convenience property for ``self.paper.width``"""
        return self.paper.width

    @property
    def height(self):
        """PointUnit: The height of the page. This is a convenience property for ``self.paper.height``"""
        return self.paper.height

    @property
    def left_edge_pos(self):
        """PointUnit: The scene-space position of the left edge of this Page"""
        return self.document.x_of_page(self)

    @property
    def right_edge_pos(self):
        """PointUnit: The scene-space position of the left edge of this Page"""
        return self.left_edge_pos + self.width

    @property
    def top_edge_pos(self):
        """PointUnit: The scene-space position of the left edge of this Page"""
        # Currently assumes that pages will be rooted at y=0 in scene space
        return PointUnit(0)

    @property
    def bottom_edge_pos(self):
        """PointUnit: The scene-space position of the left edge of this Page"""
        # Currently assumes that pages will be rooted at y=0 in scene space
        return self.height

    @property
    def left_margin_pos(self):
        """PointUnit: The scene-space position of the left margin"""
        return self.left_edge_pos + self.paper.margin_left

    @property
    def right_margin_pos(self):
        """PointUnit: The scene-space position of the right margin"""
        return self.right_edge_pos - self.paper.margin_right

    @property
    def top_margin_pos(self):
        """PointUnit: The scene-space position of the top margin"""
        return self.top_edge_pos + self.paper.margin_top

    @property
    def bottom_margin_pos(self):
        """PointUnit: The scene-space position of the bottom margin"""
        return self.bottom_edge_pos - self.paper.margin_bottom

    def build_glyph(self):
        self.glyph = PageGlyph(self)


class PageGlyph(QGraphicsRectItem):
    def __init__(self, page):
        """
        Args:
            page (Page):
        """
        self.page = page
        QGraphicsRectItem.__init__(page.x_pos, page.y_pos, page.paper.width, page.paper.height,
                                   scene=page.document.scene)
