from typing import Optional, Union

from brown.interface.font_interface import FontInterface
from brown.utils.units import GraphicUnit, Unit


class Font:

    """A text font.

    All fonts are immutable. To get a modified version of a font, use
    `Font.modified`."""

    def __init__(
        self,
        family_name: str,
        size: Union[Unit, float],
        weight: Optional[int] = None,
        italic: bool = False,
    ):
        """
        Args:
            family_name: The font family name
            size: The size (height) of the font
            weight: The font weight on a 0-100 scale, where 50 is normal,
                lower numbers are lighter, and higher are darker.
                If `None` (the default), a normal weight will be used.
            italic: Whether or not the font is italicized
        """
        self._family_name = family_name
        self._size = size if isinstance(size, Unit) else GraphicUnit(size)
        self._weight = weight
        self._italic = italic
        self._interface = FontInterface(
            self.family_name, self.size, self.weight, self.italic
        )

    ######## PUBLIC PROPERTIES ########

    @property
    def family_name(self):
        return self._family_name

    @property
    def size(self):
        return self._size

    @property
    def weight(self):
        return self._weight

    @property
    def italic(self):
        return self._italic

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

    ######## PUBLIC METHODS ########

    def modified(self, family_name=None, size=None, weight=None, italic=None):
        return Font(
            family_name if family_name is not None else self.family_name,
            size if size is not None else self.size,
            weight if weight is not None else self.weight,
            italic if italic is not None else self.italic,
        )

    def bounding_rect_of(self, string):
        """Approximate the bounding rect of a string in this font.

        Args:
            string (str): The string to derive the rect from

        Returns:
            Rect[Unit]: a bounding rectangle.
        """
        return self._interface.bounding_rect_of(string)
