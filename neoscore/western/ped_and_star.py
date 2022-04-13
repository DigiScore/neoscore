from __future__ import annotations

from typing import Optional, cast

from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.point import ORIGIN, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner_2d import Spanner2D


class PedAndStar(PositionedObject, Spanner2D, HasMusicFont):

    """Pedal notation in the ornate 'Ped' and release star style."""

    def __init__(
        self,
        start: PointDef,
        start_parent: PositionedObject,
        end_pos: PointDef,
        end_parent: Optional[PositionedObject] = None,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            start: The position of the start-pedal mark relative to ``start_parent``.
            start_parent: Anchor for the start-pedal mark.
            end_pos: The position of the release-pedal mark relative to ``end_parent``.
            end_parent: An optional anchor for the release-pedal mark.
                Defaults to ``self``.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        PositionedObject.__init__(self, start, start_parent)
        Spanner2D.__init__(
            self,
            end_pos,
            cast(PositionedObject, end_parent) if end_parent else self,
        )

        if font is None:
            font = HasMusicFont.find_music_font(start_parent)
        self._music_font = font

        # Add opening pedal mark
        self.depress_mark = MusicText(ORIGIN, self, "keyboardPedalPed", font)
        self.lift_mark = MusicText(
            self.end_pos, self.end_parent, "keyboardPedalUp", font
        )

    @property
    def music_font(self) -> MusicFont:
        return self._music_font
