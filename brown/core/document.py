from brown.config import config
from brown.utils.point import Point
from brown.utils.units import Mm
from brown.utils.rect import Rect
from brown.core.paper import Paper
from brown.core.graphic_object import GraphicObject


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

    @property
    def occupied_pages(self):
        """iter[int]: The nonempty pages in the document.

        This iterator includes any blank pages between occupied pages as well.

        Warning: This is a computationally expensive calculation
        """
        min_page, max_page = Document._min_max_pages(self.children)
        # Be sure to include max page in the range() by adding 1
        return range(min_page, max_page + 1)

    ######## PRIVATE PROPERTIES ########

    @property
    def _page_display_gap(self):
        """float: The visual horizontal gap between pages, in pixels."""
        return Mm(150)

    ######## PRIVATE METHODS ########

    @staticmethod
    def _min_max_pages(graphic_objects):
        """Find the min and max pages of an iterable of GraphicObjects

        Args:
            graphic_objects (iter[GraphicObject]):

        Returns: tuple(int, int): (min, max)
        """
        min_page = float('inf')
        max_page = -float('inf')
        for current in graphic_objects:
            current_page = GraphicObject.map_from_origin(current).page
            if current.children:
                child_min_max = Document._min_max_pages(current.children)
                min_page = min(min_page,
                               current_page,
                               child_min_max[0])
                max_page = max(max_page, current_page, child_min_max[1])
            else:
                min_page = min(min_page,
                               current_page)
                max_page = max(max_page, current_page)
        return min_page, max_page

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

    def _page_origin_in_canvas_space(self, page_number):
        """Find the origin point of a given page number.

        The origin is the top left corner of the live area, equivalent to
        the real page corner + margins and gutter.

        Args:
            page_number (int): The number of the page to locate,
                where 0 is the first page.

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
        page_origin = self._page_origin_in_canvas_space(pos.page)
        return Point(page_origin.x + pos.x, page_origin.y + pos.y, 0)

    ######## PUBLIC METHODS ########

    def page_bounding_rect(self, page_number):
        """Find the bounding rect of a page in the document, in canvas space.

        The resulting rect will cover the *live page area* - that is,
        the area within the margins of the page

        All points in the resulting rect will have page=0,
        as this is considered in canvas space.

        Args:
            page_number (int):

        Returns: Rect
        """
        page_origin = self._page_origin_in_canvas_space(page_number)
        return Rect(
            page_origin.x,
            page_origin.y,
            self.paper.live_width,
            self.paper.live_height
        )

    def render(self):
        """Render all items in the document.

        Returns: None
        """
        for child in self.children:
            child.render()
