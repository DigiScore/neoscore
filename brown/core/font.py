from brown.interface.impl.qt import font_interface_qt


class Font:

    _interface_class = font_interface_qt.FontInterfaceQt

    def __init__(self, family_name, size, weight=1, italic=False):
        self.family_name = family_name
        self.size = size
        self.weight = weight
        self.italic = italic
        self._interface = Font._interface_class(self.family_name,
                                                self.size,
                                                self.weight,
                                                self.italic)

    ######## PUBLIC PROPERTIES ########

    @property
    def ascent(self):
        return self._interface.ascent

    @property
    def descent(self):
        return self._interface.descent
