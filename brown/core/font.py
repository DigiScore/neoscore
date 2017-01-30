from brown.interface.font_interface import FontInterface


class Font:

    _interface_class = FontInterface

    def __init__(self, family_name, size, weight=1, italic=False):
        self.family_name = family_name
        self.size = size
        self.weight = weight
        self.italic = italic
        self._interface = type(self)._interface_class(self.family_name,
                                                      self.size,
                                                      self.weight,
                                                      self.italic)

    ######## PUBLIC PROPERTIES ########

    @property
    def ascent(self):
        """GraphicUnit: The ascent of the font.

        The ascent is the vertical distance between the font baseline and
        the highest any font characters reach.
        """
        return self._interface.ascent

    @property
    def descent(self):
        """GraphicUnit: The descent of the font.

        The ascent is the vertical distance between the font baseline and
        the lowest any font characters reach.
        """
        return self._interface.descent

    @property
    def em_size(self):
        """GraphicUnit: The em size for the font."""
        return self._interface.em_size

    # TODO: May need to handle size changes. In this case, be sure
    #       to update cached em_size in MusicFont subclass.
