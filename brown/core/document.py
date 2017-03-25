from brown import config
from brown.core.paper import Paper
from brown.core.page_supplier import PageSupplier
from brown.utils.point import Point
from brown.utils.rect import Rect
from brown.utils.units import Mm, GraphicUnit


class Document:

    """The document root object.

    This object should not be created directly by users - it is instantiated
    by `brown.setup()`, which creates a global instance of this class which
    can be then accessed as `brown.document`.

    This object should be created by `brown.setup()`

    NOTE: Paper gutters are not yet implemented
    """

    def __init__(self, paper=None):
        """
        Args:
            paper (Paper): The paper to use in the document. If None,
                this defaults to config.DEFAULT_PAPER_TYPE
        """
        if paper is None:
            try:
                self.paper = Paper.from_template(config.DEFAULT_PAPER_TYPE)
            except KeyError:
                raise config.InvalidConfigError(
                    'DEFAULT_PAPER_TYPE of {} is not supported'.format(
                        config.DEFAULT_PAPER_TYPE))
        else:
            self.paper = paper
        self._pages = PageSupplier(self)
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
    def pages(self):
        """PageSupplier: The `Page`s in the document.

        Pages are created on-demand by accessing this property.

        This property can be treated like a managed list:

            >>> from brown.core import brown; brown.setup()
            >>> len(brown.document.pages)             # No pages exist yet
            0
            >>> first_page = brown.document.pages[0]  # Get the first page
            >>> len(brown.document.pages)             # One page now exists
            1
            >>> sixth_page = brown.document.pages[5]  # Get the sixth page
            >>> len(brown.document.pages)             # 5 new pages are created
            6

            # Pages can be accessed by negative indexing too
            >>> assert(first_page == brown.document.pages[-6])
            >>> assert(sixth_page == brown.document.pages[-1])

        For more information on this object, see `PageSupplier`.

        This property (and the pages accessed through it)
        should be treated as read-only.
        """
        return self._pages

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
        min_page, max_page = self._min_max_pages(self.children)
        # Include the last page in range() by adding 1
        return range(min_page, max_page + 1)

    ######## PRIVATE PROPERTIES ########

    @property
    def _page_display_gap(self):
        """float: The visual horizontal gap between pages, in pixels."""
        # TODO: Move to config
        return Mm(150)

    ######## PRIVATE METHODS ########

    def _min_max_pages(self, graphic_objects):
        """Find the min and max pages of an iterable of GraphicObjects

        Args:
            graphic_objects (iter[GraphicObject]):

        Returns: tuple(int, int): (min, max)
        """
        min_page = float('inf')
        max_page = -float('inf')
        for current in graphic_objects:
            current_page_num = current.page_index
            if current.children:
                child_min_max = self._min_max_pages(current.children)
                min_page = min(min_page,
                               current_page_num,
                               child_min_max[0])
                max_page = max(max_page, current_page_num, child_min_max[1])
            else:
                min_page = min(min_page,
                               current_page_num)
                max_page = max(max_page, current_page_num)
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

    def _page_origin(self, page_number):
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

    def _paper_origin(self, page_number):
        """Find the paper origin point of a given page number.

        This gives the position of the top left corner of the actual
        sheet of paper - regardless of margins and gutter.

        Args:
            page_number (int): The number of the page to locate,
                where 0 is the first page.

        Returns:
            Point: The position of the paper origin of the given page.
                The page number of this Point will be 0, as this
                is considered relative to the document's origin.
        """
        return Point(
            (self.paper.width + self._page_display_gap) * page_number,
            GraphicUnit(0)
        )

    ######## PUBLIC METHODS ########

    def canvas_pos_of(self, graphic_object):
        """Find the paged document position of a GraphicObject.

        Args:
            graphic_object (GraphicObject): Any object in the document.

        Returns: Point: The object's paged position relative to the document.
        """
        pos = Point(GraphicUnit(0), GraphicUnit(0))
        current = graphic_object
        while current != self:
            pos += current.pos
            current = current.parent
            if type(current).__name__ == 'FlowableFrame':
                # If the parent is a flowable frame,
                # let it decide where this point goes.
                return current._map_to_canvas(pos)
        return pos

    def page_bounding_rect(self, page_number):
        """Find the bounding rect of a page in the document.

        The resulting rect will cover the *live page area* - that is,
        the area within the margins of the page

        All points in the resulting rect will have page=0,
        as this is considered in canvas space.

        Args:
            page_number (int):

        Returns: Rect
        """
        page_origin = self._page_origin(page_number)
        return Rect(
            page_origin.x,
            page_origin.y,
            self.paper.live_width,
            self.paper.live_height
        )

    def paper_bounding_rect(self, page_number):
        """Find the paper bounding rect of a page in the document.

        The resulting rect will cover the entire paper sheet -
        regardless of margins and gutter.

        All points in the resulting rect will have page=0,
        as this is considered in canvas space.

        Args:
            page_number (int):

        Returns: Rect
        """
        paper_origin = self._paper_origin(page_number)
        return Rect(
            paper_origin.x,
            paper_origin.y,
            self.paper.width,
            self.paper.height
        )

    def render(self):
        """Render all items in the document.

        Returns: None
        """
        for child in self.children:
            child.render()
