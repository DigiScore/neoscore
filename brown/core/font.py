from brown.interface.font_interface import FontInterface


class Font:

    _interface_class = FontInterface

    def __init__(self, family_name, size, weight=1, italic=False):
        """
        Args:
            family_name (str): The font family name
            size (Unit): The size (height) of the font
            weight (float): The font weight, where 1 is normal
            italic (bool): Whether or not the font is italicized
        """
        self.family_name = family_name
        self.size = size
        self.weight = weight
        self.italic = italic
        self._interface = Font._interface_class(self.family_name,
                                                self.size,
                                                self.weight,
                                                self.italic)

    ######## CONSTRUCTORS ########

    @classmethod
    def deriving(cls,
                 existing_font,
                 family_name=None,
                 size=None,
                 weight=None,
                 italic=None):
        """Derive a Font from an existing one.

        All properties not passed in args/kwargs will be copied
        from the existing Font.

        Args:
            existing_font (Font): An existing font.
            family_name (str): The font family name
            size (int): The height, in points, of the font
            weight (float): The font weight, where 1 is normal
            italic (bool): Whether or not the font is italicized
        """
        return cls(
            family_name if family_name is not None
                else existing_font.family_name,
            size if size is not None
                else existing_font.size,
            weight if weight is not None
                else existing_font.weight,
            italic if italic is not None
                else existing_font.italic
        )

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
