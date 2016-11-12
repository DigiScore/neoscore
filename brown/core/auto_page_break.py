from brown.core.page_break import PageBreak


class AutoPageBreak(PageBreak):
    """An automatic page break. See PageBreak for further docs."""

    ######## PRIVATE PROPERTIES ########

    @property
    def _is_automatic(self):
        return True
