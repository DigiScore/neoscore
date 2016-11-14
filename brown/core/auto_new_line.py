from brown.core.new_line import NewLine


class AutoNewLine(NewLine):
    """An automatic line break. See NewLine for further docs."""

    ######## PRIVATE PROPERTIES ########

    @property
    def _is_automatic(self):
        return True
