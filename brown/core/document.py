from brown.config import config
from brown.core import brown
from brown.utils.point import Point
from brown.core.paper import Paper
from brown.utils.units import Mm



class Document:

    def __init__(self, paper=None):
        if paper is None:
            try:
                self.paper = Paper.from_template(config.DEFAULT_PAPER_TYPE)
            except KeyError:
                raise config.InvalidConfigError(
                    'DEFAULT_PAPER_TYPE of {} is not supported'.format(
                        config.DEFAULT_PAPER_TYPE))
        else:
            self.paper = paper

    ######## PUBLIC PROPERTIES ########

    @property
    def paper(self):
        """Paper: The paper type of the document"""
        return self._paper

    @paper.setter
    def paper(self, value):
        self._paper = value

    ######## PRIVATE PROPERTIES ########

    @property
    def _page_display_gap(self):
        """float: The visual horizontal gap between pages, in pixels."""
        return Mm(15)

    ######## PRIVATE METHODS ########

    def _page_origin_in_doc_space(self, page_number):
        """Find the position in pixels of the origin of the live area of a page.

        The origin is the top left corner of the live area, equivalent to
        the real page corner plus margins and gutter.

        Args:
            page_number (int): The number of the page to locate

        Returns: tuple(float, float): An x, y coordinate in pixels
        Returns:
            Point: A point in pixels

        Note: Assumes left-to right layout
        """
        if page_number < 1:
            raise ValueError('page_number must be 1 or greater.')
        # Left edge of paper (not including margin/gutter)
        x_page_left = ((self.paper.width + self._page_display_gap) *
                       (page_number - 1))
        x_page_origin = x_page_left + self.paper.margin_left
        y_page_origin = self.paper.margin_top
        return Point(x_page_origin, y_page_origin)
