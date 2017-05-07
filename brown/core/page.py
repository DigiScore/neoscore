from brown.utils.point import Point


class Page:

    """A document page.

    All manually created `GraphicObject`s will have a `Page` as their
    ancestor. All `Page`s are children of the global document.

    `Page` objects are automatically created by `Document` and should
    not be manually created or manipulated.

    This class shares many properties and methods with GraphicObject,
    but notably is not a subclass of it.
    """

    def __init__(self, pos, document, page_index, paper):
        """
        Args:
            pos (Point or init tuple): The position of the top left corner
                of this page in canvas space. Note that this refers to the
                real corner of the page, not the corner of its live area
                within the paper margins.
            document (Document): The global document. This is used as
                the Page object's parent.
            page_index (int): The index of this page. This should be
                the same index this Page can be found at in the document's
                `PageSupplier`. This should be a positive number.
            paper (Paper): The type of paper this page uses.
        """
        self.pos = pos if isinstance(pos, Point) else Point(*pos)
        self._document = document
        self._page_index = page_index
        self.paper = paper
        self.children = set()

    @property
    def parent(self):
        """Document: The document this page belongs in."""
        return self._document

    @property
    def descendants(self):
        """iter[GraphicObject]: All of the objects in the children subtree.

        This recursively searches all of the object's children
        (and their children, etc.) and provides an iterator over them.

        The current implementation performs a simple recursive DFS over
        the tree, and has the potential to be rather slow.
        """
        for child in self.children:
            for subchild in child.children:
                yield subchild
            yield child

    @property
    def page_index(self):
        """The index of this page in its managing `PageSupplier` object."""
        return self._page_index

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

    def _render(self):
        """Render every object in the page.

        Returns: None
        """
        for child in self.children:
            child._render()

    def descendants_with_class_or_subclass(self, graphic_object_class):
        """Yield all child descendants with a given class or its subclasses.

        Args: graphic_object_class (type): The type to search for.
            This should be a subclass of GraphicObject.

        Yields: GraphicObject
        """
        for descendant in self.descendants:
            if isinstance(descendant, graphic_object_class):
                yield descendant

    def descendants_with_exact_class(self, graphic_object_class):
        """Yield all child descendants with a given class.

        Args: graphic_object_class (type): The type to search for.
            This should be a subclass of GraphicObject.

        Yields: GraphicObject
        """
        for descendant in self.descendants:
            if type(descendant) == graphic_object_class:
                yield descendant
