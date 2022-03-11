from typing import Optional

from neoscore.core.graphic_object import GraphicObject
from neoscore.core.mapping import map_between
from neoscore.core.music_char import MusicChar
from neoscore.core.music_text import MusicText
from neoscore.core.object_group import ObjectGroup
from neoscore.core.path import Path
from neoscore.core.pen import NO_PEN, Pen
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.spanner import Spanner
from neoscore.core.staff_object import StaffObject
from neoscore.interface.text_interface import TextInterface
from neoscore.models.interval import Interval
from neoscore.models.transposition import Transposition
from neoscore.utils.point import ORIGIN, Point, PointDef
from neoscore.utils.units import ZERO, Unit


class OctaveLine(ObjectGroup, Spanner, StaffObject):

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
        start_parent: GraphicObject,
        end_x: Unit,
        end_parent: Optional[GraphicObject] = None,
        indication: str = "8va",
    ):
        """
        Args:
            start (Point or tuple init args):
            start_parent (GraphicObject): An object either in a Staff or
                a staff itself. This object will become the line's parent.
            end_x (Unit): The spanner end x position. The y position will be
                automatically calculated to be horizontal.
            end_parent (GraphicObject): An object either in a Staff or
                a staff itself. The root staff of this *must* be the same
                as the root staff of `start_parent`. If omitted, the
                stop point is relative to the start point.
            indication (str): A valid octave indication.
                currently supported indications are:
                    - '15ma' (two octaves higher)
                    - '8va' (one octave higher)
                    - '8vb' (one octave lower)
                    - '15mb' (two octaves lower)
                The default value is '8va'.
        """
        ObjectGroup.__init__(self, start, start_parent)
        Spanner.__init__(self, end_x, end_parent or self)
        StaffObject.__init__(self, self.parent)
        self.transposition = Transposition(OctaveLine.intervals[indication])
        self.line_text = _OctaveLineText(
            # No offset relative to ObjectGroup
            pos=ORIGIN,
            parent=self,
            length=self.length,
            indication=indication,
        )

        # Vertically center the path relative to the text
        text_rect = self.line_text.bounding_rect
        # TODO LOW line needs some padding
        path_x = text_rect.width
        path_y = text_rect.height / -2
        self.line_path = Path(
            pos=Point(path_x, path_y),
            pen=Pen(
                thickness=self.staff.music_font.engraving_defaults[
                    "octaveLineThickness"
                ],
                pattern=PenPattern.DASH,
            ),
            parent=self,
        )
        # Drawn main line part
        self.line_path.line_to(self.end_pos.x, path_y, self.end_parent)
        pos_relative_to_staff = map_between(self.staff, self)
        # Draw end hook pointing toward the staff
        hook_direction = 1 if pos_relative_to_staff.y <= ZERO else -1
        self.line_path.line_to(
            self.end_pos.x,
            (path_y + self.staff.unit(0.75 * hook_direction)),
            self.end_parent,
        )

    @property
    def length(self) -> Unit:
        return self.spanner_x_length


class _OctaveLineText(MusicText, StaffObject):
    """An octave text mark recurring at line beginnings with added parenthesis.

    This is a private class meant to be used exclusively in the context
    of an OctaveLine
    """

    def __init__(
        self, pos: PointDef, parent: GraphicObject, length: Unit, indication: str
    ):
        """
        Args:
            pos:
            parent:
            length:
            indication: A valid octave indication.
                Should be a valid entry in `OctaveLine.glyphs`.
        """
        MusicText.__init__(self, pos, OctaveLine.glyphs[indication], parent)
        StaffObject.__init__(self, parent)
        open_paren_char = MusicChar(self.font, OctaveLine.glyphs["("])
        close_paren_char = MusicChar(self.font, OctaveLine.glyphs[")"])
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
            NO_PEN.interface,
            self.brush.interface,
            self.text,
            self.font._interface,
        )
        interface.render()
        self.interfaces.append(interface)

    def _render_after_break(self, local_start_x: Unit, start: Point, stop: Point):
        interface = TextInterface(
            start,
            NO_PEN.interface,
            self.brush.interface,
            self.parenthesized_text,
            self.font._interface,
        )
        interface.render()
        self.interfaces.append(interface)

    def _render_spanning_continuation(
        self, local_start_x: Unit, start: Point, stop: Point
    ):
        interface = TextInterface(
            start,
            NO_PEN.interface,
            self.brush.interface,
            self.parenthesized_text,
            self.font._interface,
        )
        interface.render()
        self.interfaces.append(interface)
