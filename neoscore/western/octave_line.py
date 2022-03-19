from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from neoscore.core.brush import NO_BRUSH
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.object_group import ObjectGroup
from neoscore.core.path import Path
from neoscore.core.pen import NO_PEN, Pen
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner import Spanner
from neoscore.interface.text_interface import TextInterface
from neoscore.models.interval import Interval
from neoscore.models.transposition import Transposition
from neoscore.models.vertical_direction import VerticalDirection
from neoscore.utils.point import ORIGIN, Point, PointDef
from neoscore.utils.units import Unit

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class OctaveLine(ObjectGroup, Spanner, HasMusicFont):

    """An octave indication with a dashed line.

    When placed in the context of a Staff, pitched content under the spanner
    is automatically transposed accordingly. Care should be taken to ensure
    OctaveLines do not overlap with one another. If this occurs,
    the transposition reflected in the staff will be an undefined choice
    among those active.

    Supported octave indications are:
        - '15ma' (two octaves higher)
        - '8va' (one octave higher)
        - '8vb' (one octave lower)
        - '15mb' (two octaves lower)

    At the starting position the octave is written in text, followed by
    a dashed line ending in a small vertical hook pointing toward the staff.
    If the spanner goes across line breaks, the octave text is repeated
    in parenthesis at the line beginning.

    TODO LOW: The dashed line portion of this spanner overlaps with
    the '8va' text. This is an involved fix that may require
    implementing text background masking or a way to easily inject
    line continuation offsets for paths.
    """

    intervals = {
        "15ma": Interval("aP15"),
        "8va": Interval("aP8"),
        "8vb": Interval("dP8"),
        "15mb": Interval("dP15"),
    }

    glyphs = {
        "15ma": "quindicesimaAlta",
        "8va": "ottavaAlta",
        "8vb": "ottavaBassaVb",
        "15mb": "quindicesimaBassaMb",
        "(": "octaveParensLeft",
        ")": "octaveParensRight",
    }

    def __init__(
        self,
        start: PointDef,
        start_parent: Parent,
        end_x: Unit,
        end_parent: Optional[Parent] = None,
        indication: str = "8va",
        direction: VerticalDirection = VerticalDirection.DOWN,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            start: The starting point.
            start_parent: The parent for the starting position. If no font is given,
                this or one of its ancestors must implement `HasMusicFont`.
            end_x: The spanner end x position. The y position will be
                automatically calculated to be horizontal.
            end_parent: An object either in a Staff or
                a staff itself. The root staff of this *must* be the same
                as the root staff of `start_parent`. If omitted, the
                stop point is relative to the start point.
            indication: A valid octave indication.
                currently supported indications are:
                    - '15ma' (two octaves higher)
                    - '8va' (one octave higher)
                    - '8vb' (one octave lower)
                    - '15mb' (two octaves lower)
                The default value is '8va'.
            direction: The direction the line's ending hook points.
                For lines above staves, this should be down, and vice versa for below.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        ObjectGroup.__init__(self, start, start_parent)
        Spanner.__init__(self, end_x, end_parent or self)
        if font is None:
            font = HasMusicFont.find_music_font(start_parent)
        self._music_font = font
        self.direction = direction
        self.transposition = Transposition(OctaveLine.intervals[indication])
        self.line_text = _OctaveLineText(ORIGIN, self, self.length, indication, font)

        # Vertically center the path relative to the text
        text_rect = self.line_text.bounding_rect
        # TODO LOW line needs some padding
        path_x = text_rect.width
        path_y = cast(Unit, text_rect.height / -2)
        self.line_path = Path(
            Point(path_x, path_y),
            self,
            NO_BRUSH,
            Pen(
                thickness=font.engraving_defaults["octaveLineThickness"],
                pattern=PenPattern.DASH,
            ),
        )
        # Drawn main line part
        self.line_path.line_to(self.end_pos.x, path_y, self.end_parent)
        self.line_path.line_to(
            self.end_pos.x,
            (path_y + font.unit(0.75 * self.direction.value)),
            self.end_parent,
        )

    @property
    def music_font(self) -> MusicFont:
        return self._music_font

    @property
    def length(self) -> Unit:
        return self.spanner_x_length


class _OctaveLineText(MusicText):
    """An octave text mark recurring at line beginnings with added parenthesis.

    This is a private class meant to be used exclusively in the context
    of an OctaveLine
    """

    def __init__(
        self,
        pos: PointDef,
        parent: PositionedObject,
        length: Unit,
        indication: str,
        font: MusicFont,
    ):
        MusicText.__init__(self, pos, parent, OctaveLine.glyphs[indication], font)
        open_paren_char = MusicChar(self.music_font, OctaveLine.glyphs["("])
        close_paren_char = MusicChar(self.music_font, OctaveLine.glyphs[")"])
        self.parenthesized_text = (
            open_paren_char.codepoint + self.text + close_paren_char.codepoint
        )
        self._length = length

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self) -> Unit:
        return self._length

    ######## PRIVATE METHODS ########

    def _render_before_break(
        self, local_start_x: Unit, start: Point, stop: Point, dist_to_line_start: Unit
    ):
        interface = TextInterface(
            start,
            self.brush.interface,
            NO_PEN.interface,
            self.text,
            self.font.interface,
        )
        interface.render()
        self.interfaces.append(interface)

    def _render_after_break(self, local_start_x: Unit, start: Point):
        interface = TextInterface(
            start,
            self.brush.interface,
            NO_PEN.interface,
            self.parenthesized_text,
            self.font.interface,
        )
        interface.render()
        self.interfaces.append(interface)

    def _render_spanning_continuation(
        self, local_start_x: Unit, start: Point, stop: Point
    ):
        interface = TextInterface(
            start,
            self.brush.interface,
            NO_PEN.interface,
            self.parenthesized_text,
            self.font.interface,
        )
        interface.render()
        self.interfaces.append(interface)
