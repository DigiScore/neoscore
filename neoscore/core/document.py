from collections.abc import Callable

from neoscore import constants
from neoscore.core.page_supplier import PageSupplier
from neoscore.core.paper import Paper
from neoscore.core.point import Point
from neoscore.core.units import ZERO


class Document:

    """The document root object.

    This object should not be created directly by users - it is instantiated
    by `neoscore.setup()`, which creates a global instance of this class which
    can be then accessed as `neoscore.document`.
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

            >>> from neoscore.core import neoscore; neoscore.setup()
            >>> len(neoscore.document.pages)             # No pages exist yet
            0
            >>> first_page = neoscore.document.pages[0]  # Get the first page
            >>> len(neoscore.document.pages)             # One page now exists
            1
            >>> sixth_page = neoscore.document.pages[5]  # Get the sixth page
            >>> len(neoscore.document.pages)             # 5 new pages are created
            6

            # Pages can be accessed by negative indexing too
            >>> assert(first_page == neoscore.document.pages[-6])
            >>> assert(sixth_page == neoscore.document.pages[-1])
            >>> neoscore.shutdown()

        For more information on this object, see `PageSupplier`.
        """
        return self._pages

    ######## PRIVATE METHODS ########

    def _run_on_all_descendants(self, func: Callable):
        for page in self.pages:
            for obj in page.descendants:
                func(obj)

    def _render(self):
        """Render all items in the document.

        Returns: None
        """
        self._run_on_all_descendants(lambda g: g._pre_render_hook())
        for page in self.pages:
            page._render()
        self._run_on_all_descendants(lambda g: g._post_render_hook())

    ######## PUBLIC METHODS ########

    def page_origin(self, page_index: int) -> Point:
        """Find the origin point of a given page number.

        The origin is the top left corner of the live page area.

        Args:
            page_index: The 0-based index of the page to locate.
        """
        page_x = (self.paper.width + constants.PAGE_DISPLAY_GAP) * page_index
        return Point(page_x, ZERO)
