from brown.config import config
from brown.utils.point import Point
from brown.core.paper import Paper
from brown.utils.units import Mm


class Document:

    "The document root object."""

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
        self._children = set()

    ######## PUBLIC PROPERTIES ########

    @property
    def paper(self):
        """Paper: The paper type of the document"""
        return self._paper

    @paper.setter
    def paper(self, value):
        self._paper = value

    @property
    def children(self):
        """set{GraphicObject}: All objects who have self as their parent."""
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    ######## PRIVATE PROPERTIES ########

    @property
    def _page_display_gap(self):
        """float: The visual horizontal gap between pages, in pixels."""
        return Mm(15)

    ######## PRIVATE METHODS ########

    def _register_child(self, child):
        """Add an object to `self.children`.

        Args:
            child (GraphicObject): The object to add

        Returns: None
        """
        self.children.add(child)

    def _unregister_child(self, child):
        """Remove an object from `self.children`.

        Args:
            child (GraphicObject): The object to remove

        Returns: None
        """
        self.children.remove(child)

    def _page_origin_in_doc_space(self, page_number):
        """Find the origin point of a given page number.

        The origin is the top left corner of the live area, equivalent to
        the real page corner + margins and gutter.

        Document page numbers are counted where 0 is the first page.

        Args:
            page_number (int): The number of the page to locate.

        Returns:
            Point: The position of the origin of the given page.
                The page number of this Point will be 0, as this
                is considered relative to the document's origin.
        """
        # Left edge of paper (not including margin/gutter)
        x_page_left = ((self.paper.width + self._page_display_gap) *
                       (page_number))
        x_page_origin = x_page_left + self.paper.margin_left
        y_page_origin = self.paper.margin_top
        return Point(x_page_origin, y_page_origin)

    def _map_to_canvas(self, pos):
        """Find the global document position of a given point.

        The resulting Point will have the page number of 0.

        Args:
            pos (Point):

        Returns: Point:
        """
        page_origin = self._page_origin_in_doc_space(pos.page)
        return Point(page_origin.x + pos.x, page_origin.y + pos.y, 0)

    ######## PUBLIC METHODS ########

    def render(self):
        """Render all items in the document.

        Returns: None
        """
        for child in self.children:
            child.render()
