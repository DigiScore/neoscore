#!/usr/bin/env python

from .exceptions import PageNotInDocumentError, NoPageAtCoordinateError
from .paper import Paper
from .page import Page
from .point_unit import PointUnit


class Document:
    """
    A document containing a list of Page objects
    """

    def __init__(self, default_paper, scene, page_gap=36):
        """
        Args:
            default_paper (Paper or str): str values must be a valid argument
                to ``Paper.from_default_paper_type()``
            scene (QGraphicsScene): The scene in which this Document belongs
            page_list (None, list[Paper], or Paper: The list of Page objects
                contained in this Document
            page_gap (PointUnit or int): The visual gap between pages displayed
                in this Document
        """
        # TODO: have default_paper actually have a default value, and maybe
        #   redo the implementation of default_paper so it's more intuitive
        #   since it's such an uncommon case that the paper type will change
        #   within a document
        self.default_paper = default_paper
        self.scene = scene
        self._page_list = []
        self.page_gap = page_gap


    @property
    def default_paper(self):
        """Paper: The default paper type for pages within this Document"""
        return self._default_paper

    @default_paper.setter
    def default_paper(self, new_value):
        if isinstance(new_value, str):
            new_value = Paper.from_default_paper_type(new_value)
        elif isinstance(new_value, Paper):
            pass
        else:
            raise TypeError
        self._default_paper = new_value

    @property
    def page_gap(self):
        """PointUnit: The visual gap between pages"""
        return self._page_gap

    @page_gap.setter
    def page_gap(self, new_value):
        self._page_gap = PointUnit(new_value)

    @property
    def page_list(self):
        """list[Page]: The list of Page objects in this Document"""
        return self._page_list

    def append_new_page_from_last(self):
        """
        Append a new page to ``self.page_list`` using the Paper of
        the last page, and return it.

        If ``self.page_list`` is empty, create a new page from
        self.default_paper and return that.

        Returns: Page
        """
        if self.page_list:
            # If there are contents in self.page_list, work from the last page
            last_page = self.page_list[-1]
            # Currently doesn't support overridden page numbers
            self.page_list.append(Page(self, last_page.paper, last_page.document_page_number + 1))
        else:
            # Otherwise if self.page_list is empty, create a new page from self.default paper and append that
            self.page_list.append(Page(self, self.default_paper, 1))
        return self.page_list[-1]

    def get_next_page_or_extend_last(self, page):
        """
        Gets the next page in ``self.page_list`` from a given ``page``. If ``page`` is the last page in self.page_list,
        add a new page and return that.

        Args:
            page: Page

        Returns: Page
        """
        try:
            starting_page_index = self.page_list.index(page)
        except ValueError:
            raise PageNotInDocumentError
        if starting_page_index + 1 < len(self.page_list):
            # If there is an existing page after the starting page, return that
            return self.page_list[starting_page_index + 1]
        else:
            # Otherwise, build a new page and return that
            return self.append_new_page_from_last()

    def x_of_page(self, page):
        """
        Find the x coordinate of a given Page in self.page_list

        Args:
            page (Page): Must be a page contained within ``self.page_list``

        Returns: PointUnit

        Raises: PageNotInDocumentError if ``page`` is not in ``self.page_list``
        """
        try:
            # Find the page's index
            testing_page_index = self.page_list.index(page)
        except ValueError:
            # Raise exception if the page isn't in self.page_list
            raise PageNotInDocumentError
        cumulative_x = PointUnit(0)
        for i in range(testing_page_index):
            cumulative_x += self.page_list[i].width + self.page_gap
        return cumulative_x

    def x_of_document_page_number(self, document_page_number):
        """
        Find and return the x coordinate of the page at a given document page number. (Where 1 is the first page)

        Code very similar to self.x_of_page, except we add cumulative_x to find the document page number without
        the page which the document refers to necessarily being in self.page_list. This is useful for cases
        such as Page.__init__() where the page must find where it belongs without necessarily belonging in the
        document's page_list yet.

        Args:
            page_number (int): The document page number. Note that this is not necessarily the same
                as Page.display_page_number

        Returns: PointUnit
        """
        cumulative_x = PointUnit(0)
        try:
            for current_index in range(document_page_number - 1):
                cumulative_x += self.page_list[current_index].width + self.page_gap
        except ValueError:
            raise PageNotInDocumentError
        return cumulative_x

    def page_of_coordinate(self, x_pos, y_pos):
        """
        Finds which page in this Document a given scene-space coordinate lands on.

        Args:
            x_pos (PointUnit):
            y_pos (PointUnit):

        Returns: Page

        Raises: NoPageAtCoordinateError if there is no page under the given coordinate
        """
        for page in self.page_list:
            if ((page.scene_space_x_pos <= x_pos <= page.scene_space_x_pos + page.width) and
                    (page.scene_space_y_pos <= y_pos <= page.scene_space_y_pos + page.height)):
                return page
        # If we've made it this far, no such page exists.
        raise NoPageAtCoordinateError
