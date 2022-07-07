from __future__ import annotations

from typing import Optional, Union

from neoscore.core.rect import Rect
from neoscore.core.units import Unit
from neoscore.interface.font_interface import FontInterface

_BOUNDING_RECT_CACHE: Dict[Tuple[Font, str], Rect] = {}


class Font:

    """A text font.

    All fonts are immutable. To get a modified version of a font, use
    :obj:`.Font.modified`
    """

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
                If ``None`` (the default), a normal weight will be used.
            italic: Whether the font is italicized
        """
        self._family_name = family_name
        self._size = size if isinstance(size, Unit) else Unit(size)
        self._weight = weight
        self._italic = italic
        self._interface = FontInterface(
            self.family_name, self.size, self.weight, self.italic
        )

    @property
    def family_name(self) -> str:
        return self._family_name

    @property
    def size(self) -> Unit:
        return self._size

    @property
    def weight(self) -> Optional[int]:
        return self._weight

    @property
    def italic(self) -> bool:
        return self._italic

    @property
    def ascent(self) -> Unit:
        """The ascent of the font.

        The ascent is the vertical distance between the font baseline and
        the highest any font characters reach.
        """
        return self._interface.ascent

    @property
    def descent(self) -> Unit:
        """The descent of the font.

        The ascent is the vertical distance between the font baseline and
        the lowest any font characters reach.
        """
        return self._interface.descent

    @property
    def x_height(self) -> Unit:
        """The x-height for the font."""
        return self._interface.x_height

    @property
    def interface(self) -> FontInterface:
        """The backing low-level font interface"""
        return self._interface

    def __str__(self):
        return f"Font('{self.family_name}', {self.size}, {self.weight}, {self.italic})"

    def __eq__(self, other):
        return (
            isinstance(other, Font)
            and self.family_name == other.family_name
            and self.size == other.size
            and self.weight == other.weight
            and self.italic == other.italic
        )

    def __hash__(self):
        return hash(
            (self.family_name, self.size.rounded_base_value, self.weight, self.italic)
        )

    def modified(
        self,
        family_name: Optional[str] = None,
        size: Optional[Union[Unit, float]] = None,
        weight: Optional[int] = None,
        italic: Optional[bool] = None,
    ) -> Font:
        """Derive a font from this one.

        All properties not specified will be taken from the existing font.
        """
        return Font(
            family_name if family_name is not None else self.family_name,
            size if size is not None else self.size,
            weight if weight is not None else self.weight,
            italic if italic is not None else self.italic,
        )

    def bounding_rect_of(self, string: str) -> Rect:
        """Approximate the bounding rect of a string in this font."""
        key = (self, string)
        cached_rect = _BOUNDING_RECT_CACHE.get(key)
        if cached_rect:
            return cached_rect
        rect = self._interface.bounding_rect_of(string)
        _BOUNDING_RECT_CACHE[key] = rect
        return rect
