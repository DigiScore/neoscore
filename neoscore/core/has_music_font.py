from __future__ import annotations

from typing import TYPE_CHECKING, Type, cast

from neoscore.core.exceptions import NoAncestorWithMusicFontError
from neoscore.core.mapping import first_ancestor_with_attr
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import Unit

if TYPE_CHECKING:
    from neoscore.core.music_font import MusicFont


class HasMusicFont:
    """A mixin for classes which have an associated staff measurement.

    This is useful for integration with SMuFL fonts, where glyphs and
    their metadata are measured relative to a staff space.

    A naive and slow implementation of `music_font` is provided which
    returns the nearest music found in the object's
    ancestors. Subclasses will often want to override this.
    """

    @property
    def music_font(self) -> MusicFont:
        return HasMusicFont.find_music_font(cast(PositionedObject, self).parent)

    @property
    def unit(self) -> Type[Unit]:
        """A unit type where `self.unit(1)` is the size of a staff space."""
        return self.music_font.unit

    @staticmethod
    def find_music_font(obj: PositionedObject) -> MusicFont:
        """Return the music font from `obj` or its nearest ancestor with one.

        This checks `obj` and then its ancestors for whether they have
        a `music_font` attribute, returning the first value found. If
        no font is found, this raises a
        `NoAncestorWithMusicFontError`.
        """
        if hasattr(obj, "music_font"):
            return cast(HasMusicFont, obj).music_font
        try:
            lookup_result = first_ancestor_with_attr(obj, "music_font")
            if lookup_result is None:
                raise NoAncestorWithMusicFontError()
        except:
            raise NoAncestorWithMusicFontError()
        return cast(HasMusicFont, lookup_result).music_font
