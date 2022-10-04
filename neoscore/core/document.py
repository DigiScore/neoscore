from collections.abc import Callable
from typing import Optional

from neoscore.core.brush import Brush
from neoscore.core.page_supplier import PageOverlayFunc, PageSupplier
from neoscore.core.paper import Paper
from neoscore.core.point import Point
from neoscore.core.units import ZERO, Mm

_PAGE_DISPLAY_GAP = Mm(50)


class Document:

    """The document root object.

    This object should not be created directly by users - it is instantiated
    by :obj:`.neoscore.setup`, which creates a global instance of this class which
    can be then accessed as :obj:`.neoscore.document`.
    """

    def __init__(self, paper: Paper, overlay_func: Optional[PageOverlayFunc] = None):
        """
        Args:
            paper: The paper to use in the document.
            overlay_func: An optional function to run on each generated page.
        """
        self._paper = paper
        self._pages = PageSupplier(self, overlay_func)

    @property
    def paper(self) -> Paper:
        """The paper type of the document"""
        return self._paper

    @paper.setter
    def paper(self, value):
        self._paper = value

    @property
    def pages(self) -> PageSupplier:
        """The document's pages.

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
            >>> # Pages can be accessed by negative indexing too
            >>> assert(first_page == neoscore.document.pages[-6])
            >>> assert(sixth_page == neoscore.document.pages[-1])
            >>> neoscore.shutdown()

        For more information on this object, see :obj:`.PageSupplier`.
        """
        return self._pages

    def _run_on_all_descendants(self, func: Callable):
        for page in self.pages:
            for obj in page.descendants:
                func(obj)

    def render(self, display_page_geometry: bool, background_brush: Brush):
        """Render all items in the document.

        This should not be called directly.

        Args:
            display_page_geometry: Whether to include a preview of page geometry.
            background_brush: The brush used to draw the scene background.
        """
        self._run_on_all_descendants(lambda g: g.pre_render_hook())
        if display_page_geometry:
            for page in self.pages:
                page.create_geometry_preview(background_brush)
        for page in self.pages:
            page.render()
        self._run_on_all_descendants(lambda g: g.post_render_hook())

    def page_origin(self, index: int) -> Point:
        """Find the origin point of a given page number.

        The origin is the top left corner of the live page area.

        Args:
            index: The 0-based index of the page to locate.
        """
        page_x = (self.paper.width + _PAGE_DISPLAY_GAP) * index
        return Point(page_x, ZERO)
