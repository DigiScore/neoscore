from brown.core.invisible_object import InvisibleObject


class Page(InvisibleObject):

    """A document page.

    All manually created `GraphicObject`s will have a `Page` as their
    ancestor. All `Page`s are children of the global document.

    `Page` objects are automatically created by `Document` and should
    not be manually created or manipulated.
    """

    def __init__(self, pos, document, paper):
        """
        Args:
            pos (Point or init tuple): The position of the top left corner
                of this page in canvas space. Note that this refers to the
                real corner of the page, not the corner of its live area
                within the paper margins.
            document (Document): The global document. This is used as
                the Page object's parent.
            paper (Paper): The type of paper this page uses.
        """
        super().__init__(pos, parent=document)
        self.paper = paper
