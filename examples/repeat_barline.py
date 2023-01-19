from typing import List, Union

from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.music_text import MusicText
from neoscore.core.text_alignment import AlignmentX
from neoscore.core.units import Mm, Unit
from neoscore.western import barline_style
from neoscore.western.abstract_staff import AbstractStaff
from neoscore.western.barline import Barline
from neoscore.western.brace import Brace
from neoscore.western.staff import Staff
from neoscore.western.staff_group import StaffGroup
from neoscore.western.system_line import SystemLine


def repeat_barline(
    pos_x: Unit,
    staves: Union[StaffGroup, List[AbstractStaff]],
    connected: bool,
    is_end_repeat: bool = True,
) -> Barline:
    """Create a repeat barline.

    This creates a ``Barline``, internally restyles it for start-repeats if requested,
    and creates child ``MusicText`` objects for repeat dots. The repeat dots are direct
    children of the returned ``Barline``, not the staves they are aligned with.

    In the future this may be pulled directly into neoscore.

    Args:
        pos_x: The barline X position relative to the highest staff.
            If ``is_end_repeat``, this specifies the right edge of the barline.
            Otherwise it specifies the left edge.
        pos_x: The barline style
        staves: The staves spanned
        connected: Whether the barline should be connected across staves
        is_end_repeat: If true, create an end-repeat with the dots on the left side.
            Otherwise, create a start-repeat with the dots on the right and the
            thick-thin barline orientation flipped.
    """
    if is_end_repeat:
        style = barline_style.END
    else:
        style = list(reversed(barline_style.END))
    barline = Barline(pos_x, staves, style, connected)
    # We determine where the repeat dots should be horizontally positioned very hackily
    # by leveraging knowledge about how barline paths are constructed to infer where the
    # left or right edge of the path-group's bounding rect is. If neoscore had proper
    # bounding rect support this would be a lot easier.
    if is_end_repeat:
        leftmost_path = barline.paths[-1]
        dot_x = (
            leftmost_path.x
            - barline.music_font.engraving_defaults["repeatBarlineDotSeparation"]
        )
    if not is_end_repeat:
        # For start-repeat barlines, we want to position by the left edge.
        # Here we do this very hackily by leveraging knowledge about how barline
        # paths are constructed to infer where the left edge of the path-group's
        # bounding rect is. If neoscore had proper bounding rect support this would
        # be a lot easier.
        rightmost_path = barline.paths[0]
        barline.x -= rightmost_path.x
        dot_x = barline.music_font.engraving_defaults["repeatBarlineDotSeparation"]
    # Create repeat dots for every staff
    for staff in barline.staves:
        staff_y_offset = barline.map_to(staff).y
        dot_y = staff_y_offset + staff.center_y + staff.unit(2)
        dots = MusicText((dot_x, dot_y), barline, "repeatDots", barline.music_font)
        if is_end_repeat:
            dots.alignment_x = AlignmentX.RIGHT
    return barline


neoscore.setup()
staff_group = StaffGroup()
Staff((Mm(0), Mm(0)), None, Mm(100), staff_group),
Staff((Mm(0), Mm(20)), None, Mm(100), staff_group),
Staff((Mm(0), Mm(40)), None, Mm(100), staff_group, line_count=3),
Staff((Mm(0), Mm(60)), None, Mm(100), staff_group, line_count=1),
brace = Brace(staff_group)
SystemLine(staff_group)

repeat_barline(Mm(0), staff_group, True, is_end_repeat=False)
repeat_barline(Mm(100), staff_group, True, is_end_repeat=True)

render_example("repeat_barline")
