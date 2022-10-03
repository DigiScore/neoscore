from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from typing_extensions import TypeAlias

from neoscore.core.directions import DirectionX
from neoscore.core.page import Page

if TYPE_CHECKING:
    from neoscore.core.document import Document


PageOverlayFunc: TypeAlias = Callable[[Page], None]
"""A function to run on every page after creation.

The function takes one argument, the newly generated page. Functions will typically
create objects with this page as their parent.

See :obj:`.simple_header_footer` for a ready-made simple overlay function.
"""


class PageSupplier:
    """A supplier and generator-on-demand of document :obj:`.Page` objects.

    This acts like a list of ``Page`` objects which generates them as needed.
    Externally, it can be used mostly as a list. If an index is requested for which no
    page yet exists, that page will be generated, as well as any missing pages between
    the previous last page and the one requested. Consequently, keep in mind that
    innocent looking operations such as ``page_suppler[100000]`` are actually expensive
    operations, as they implicitly generate thousands of Page objects.

    The contents of the ``PageSupplier`` should be treated as immutable. Attempts to
    modify the pages it contains will likely result in unexpected behavior.

    This is an internal class meant to be created by the global :obj:`.Document` for its
    ``pages`` property.
    """

    def __init__(
        self, document: Document, overlay_func: Optional[PageOverlayFunc] = None
    ):
        """
        Args:
            document: The global document using this object.
            overlay_func: A function to call with every page when generated.
                This can be used to create headers and footers.
        """
        self._document = document
        self._page_list: List[Page] = []
        self.overlay_func = overlay_func

    def __getitem__(self, index):
        if index >= len(self._page_list):
            for new_index in range(len(self._page_list), index + 1):
                page_side = DirectionX.LEFT if new_index % 2 else DirectionX.RIGHT
                new_page = Page(
                    self.document.page_origin(new_index),
                    self.document,
                    new_index,
                    page_side,
                    self.document.paper,
                )
                self._page_list.append(new_page)
                if self.overlay_func:
                    self.overlay_func(new_page)
        return self._page_list[index]

    def __iter__(self):
        return self._page_list.__iter__()

    def __len__(self):
        return len(self._page_list)

    @property
    def document(self) -> Document:
        return self._document

    @property
    def overlay_func(self) -> Optional[PageOverlayFunc]:
        """A function to call on every page generation.

        This function is called with every generated page at the time of generation. If
        the value is changed it will only affect pages generated after the change.
        """
        return self._overlay_func

    @overlay_func.setter
    def overlay_func(self, value: Optional[PageOverlayFunc]):
        self._overlay_func = value
