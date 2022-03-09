from collections.abc import Callable

from brown import constants
from brown.core.page_supplier import PageSupplier
from brown.core.paper import Paper
from brown.utils.point import Point
from brown.utils.rect import Rect
from brown.utils.units import ZERO, Unit


class Document:

    """The document root object.

    This object should not be created directly by users - it is instantiated
    by `brown.setup()`, which creates a global instance of this class which
    can be then accessed as `brown.document`.

    NOTE: Paper gutters are not yet implemented
    """

    def __init__(self, paper: Paper):
        """
        Args:
            paper: The paper to use in the document.
        """
        self._paper = paper
        self._pages = PageSupplier(self)

    ######## PUBLIC PROPERTIES ########

    @property
    def paper(self) -> Paper:
        """The paper type of the document"""
        return self._paper

    @paper.setter
    def paper(self, value):
        self._paper = value

    @property
    def pages(self) -> PageSupplier:
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
        """
        return self._pages

    ######## PRIVATE PROPERTIES ########

    @property
    def _page_display_gap(self) -> Unit:
        """The visual horizontal gap between pages on the canvas.

        This only affects page display in the rendered preview,
        and has no effect on exported documents.
        """
        return constants.PAGE_DISPLAY_GAP

    ######## PRIVATE METHODS ########

    def _run_on_all_grobs(self, func: Callable):
        for page in self.pages:
            for grob in page.descendants:
                func(grob)

    def _render(self):
        """Render all items in the document.

        Returns: None
        """
        self._run_on_all_grobs(lambda g: g._pre_render_hook())
        for page in self.pages:
            page._render()
        self._run_on_all_grobs(lambda g: g._post_render_hook())

    ######## PUBLIC METHODS ########

    def page_origin(self, page_number: int) -> Point:
        """Find the origin point of a given page number.

        The origin is the top left corner of the live area, equivalent to
        the real page corner + margins and gutter.

        Args:
            page_number: The number of the page to locate,
                where 0 is the first page.

        Returns: The position of the origin of the given page.  The
            page number of this Point will be 0, as this is considered
            relative to the document's origin.
        """
        # Left edge of paper (not including margin/gutter)
        x_page_left: Unit = (self.paper.width + self._page_display_gap) * page_number
        x_page_origin: Unit = x_page_left + self.paper.margin_left
        y_page_origin = self.paper.margin_top
        return Point(x_page_origin, y_page_origin)

    def paper_origin(self, page_number: int) -> Point:
        """Find the paper origin point of a given page number.

        This gives the position of the top left corner of the actual
        sheet of paper - regardless of margins and gutter.

        Args:
            page_number (int): The number of the page to locate,
                where 0 is the first page.

        Returns: The position of the paper origin of the given page.
            The page number of this Point will be 0, as this is
            considered relative to the document's origin.
        """
        return Point((self.paper.width + self._page_display_gap) * page_number, ZERO)

    def page_bounding_rect(self, page_number: int) -> Rect:
        """Find the bounding rect of a page in the document.

        The resulting rect will cover the *live page area* - that is,
        the area within the margins of the page
        """
        page_origin = self.page_origin(page_number)
        return Rect(
            page_origin.x, page_origin.y, self.paper.live_width, self.paper.live_height
        )

    def paper_bounding_rect(self, page_number: int) -> Rect:
        """Find the paper bounding rect of a page in the document.

        The resulting rect will cover the entire paper sheet -
        regardless of margins and gutter.

        Args:
            page_number (int):

        Returns: Rect
        """
        paper_origin = self.paper_origin(page_number)
        return Rect(paper_origin.x, paper_origin.y, self.paper.width, self.paper.height)
