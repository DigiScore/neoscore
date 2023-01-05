"""
This example demonstrates slightly more complicated mouse and keyboard input
in the interactive runtime viewport.
"""

from typing import List, Optional

from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.key_event import KeyEventType
from neoscore.core.mouse_event import MouseEventType
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.point import Point
from neoscore.core.text import Text
from neoscore.core.units import Mm, Unit

"""
This example shows what keys are being held down and displays them on the center of 
the screen. It also allows the user to click-and-drag to generate line-segments.

There are a few caveats that must be worked around to get this example working, both 
related to the viewport. The viewport by default shifts to accomodate new elements as 
they are added to the page. To restrict viewport movement, we create an arbitrarily 
large invisible rectangle. To generate line-segments where we click on the screen, 
the page coordinates and screen coordinates should be identical. One way to achieve 
this is by fixing the size and scale of the viewport.
"""

DEFAULT_TEXT_STR = "To interact with the scene, press keys or click and drag the mouse"

scene_changed = False
"""Global variable tracking whether the scene changed and requires a re-render.

This is used to demonstrate the optimization of using RefreshFuncResult to tell neoscore
when it does and doesn't need to re-render the scene. See RefreshFuncResult to learn
more about this.
"""


def key_handler(event):
    """
    Key event handler.

    Add single characters to a list when a key is pressed,
    and remove them from the list when the key is released.
    """
    global held_key_strings
    global scene_changed
    if event.event_type == KeyEventType.PRESS:
        held_key_strings.append(event.text)
    if event.event_type == KeyEventType.RELEASE:
        held_key_strings.remove(event.text)
    typing_text.text = (
        " ".join(held_key_strings) if held_key_strings else DEFAULT_TEXT_STR
    )
    scene_changed = True


def mouse_handler(event):
    """
    Mouse event handler and path creator.

    Remember where the user clicked the mouse, then
    draw a line between the click and release points when the mouse is released."""
    global click_point
    global scene_changed
    if event.event_type == MouseEventType.PRESS:
        click_point = event.document_pos
    elif event.event_type == MouseEventType.RELEASE:
        if click_point is None:
            print("Ignoring unexpected mouse RELEASE event")
            return
        path = Path(click_point, None, "#ff00ff55")
        release_pos_relative_to_click = event.document_pos - click_point
        path.line_to(release_pos_relative_to_click.x, release_pos_relative_to_click.y)
        click_point = None
        scene_changed = True


def refresh_func(time: float) -> neoscore.RefreshFuncResult:
    global scene_changed
    result = neoscore.RefreshFuncResult(scene_changed)
    scene_changed = False  # Reset before returning
    return result


neoscore.setup()
Path.rect(
    (Mm(-1000000), Mm(-1000000)),
    None,
    Mm(2000000),
    Mm(2000000),
    Brush.no_brush(),
    Pen.no_pen(),
)

click_point: Optional[Point] = None
held_key_strings: List[str] = []
typing_text = Text((Unit(20), Unit(250)), None, DEFAULT_TEXT_STR)


neoscore.set_key_event_handler(key_handler)
neoscore.set_mouse_event_handler(mouse_handler)
neoscore.set_viewport_center_pos((Unit(250), Unit(250)))
neoscore.show(
    refresh_func,
    auto_viewport_interaction_enabled=False,
    display_page_geometry=False,
    min_window_size=(500, 500),
    max_window_size=(500, 500),
)
