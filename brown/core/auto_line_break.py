from brown.core.line_break import LineBreak


class AutoLineBreak(LineBreak):
    """An automatic line break. See LineBreak for further docs."""

    ######## PRIVATE PROPERTIES ########

    @property
    def _is_automatic(self):
        return True
