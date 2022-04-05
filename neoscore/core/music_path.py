from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.brush import BrushDef
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_font import MusicFont
from neoscore.core.path import Path
from neoscore.core.pen import PenDef
from neoscore.core.point import PointDef

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class MusicPath(Path, HasMusicFont):
    """A Path with a music font.

    This is mostly useful as a superclass for paths which use a
    MusicFont's engraving defaults and staff unit to control their
    appearance, but it can also be instantiated directly.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[Parent] = None,
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """
        Args:
            pos: The position of the path root.
            parent: The parent object. If no font is given, this or one of its
                ancestors must implement `HasMusicFont`.
            font: If provided, this overrides any font found in the ancestor chain.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with.
        """
        Path.__init__(self, pos, parent, brush, pen)
        if font is None:
            font = HasMusicFont.find_music_font(parent)
        self._music_font = font

    @property
    def music_font(self) -> MusicFont:
        return self._music_font
