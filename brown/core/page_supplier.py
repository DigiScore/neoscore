from brown.core.page import Page


class PageSupplier:
    """A supplier and generator-on-demand of document Page objects.

    This acts like a list of Page objects which generates them as
    needed. Externally, it can be used mostly as a list. If an index
    is requested for which no Page yet exists, that page will be
    generated, as well as any missing pages between the previous
    last page and the one requested. Consequently, keep in mind
    that innocent looking operations such as some_page_suppler[100000]
    are actually expensive operations, as they implicitly generate
    thousands of Page objects.

    The contents of the PageSupplier should be treated as immutable.
    Attempts to modify the pages it contains will likely result in
    unexpected behavior.

    This is an internal class meant to be created by the global Document
    for its `pages` property.
    """
    def __init__(self, document):
        """
        Args:
            document (Document): The global document using this object.
        """
        self.document = document
        self._page_list = []

    def __getitem__(self, index):
        if index >= len(self._page_list):
            for new_index in range(len(self._page_list), index + 1):
                self._page_list.append(
                    Page(self.document.page_origin(new_index),
                         self.document,
                         new_index,
                         self.document.paper))
        return self._page_list[index]

    def __iter__(self):
        return self._page_list.__iter__()

    def __len__(self):
        return len(self._page_list)
