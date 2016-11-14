from brown.core.new_page import NewPage


class AutoNewPage(NewPage):
    """An automatic page break. See NewPage for further docs."""

    ######## PRIVATE PROPERTIES ########

    @property
    def _is_automatic(self):
        return True
