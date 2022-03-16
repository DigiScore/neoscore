from __future__ import annotations

from typing import TYPE_CHECKING

from neoscore.core.paper import Paper
from neoscore.core.positioned_object import PositionedObject
from neoscore.utils.point import PointDef

if TYPE_CHECKING:
    from neoscore.core.document import Document


class Page(PositionedObject):

    """A document page.

    All manually created `PositionedObject`s will have a `Page` as their
    ancestor. All `Page`s are children of the global document.

    `Page` objects are automatically created by `Document` and should
    not be manually created or manipulated.
    """

    def __init__(
        self, pos: PointDef, document: Document, page_index: int, paper: Paper
    ):
        """
        Args:
            pos: The position of the top left corner
                of this page in canvas space. Note that this refers to the
                real corner of the page, not the corner of its live area
                within the paper margins.
            document: The global document. This is used as
                the Page object's parent.
            page_index: The index of this page. This should be
                the same index this Page can be found at in the document's
                `PageSupplier`. This should be a positive number.
            paper: The type of paper this page uses.
        """
        super().__init__(pos, document)
        self._document = document
        self._page_index = page_index
        self.paper = paper
        self.children = []

    @property
    def page_index(self):
        """The index of this page in its managing `PageSupplier` object."""
        return self._page_index
