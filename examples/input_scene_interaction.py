"""
This example demonstrates slightly more complicated mouse and keyboard input
in the interactive runtime viewport.
"""

from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.key_event import KeyEventType
from neoscore.core.mouse_event import MouseEventType
from neoscore.core.path import Path
from neoscore.core.pen import Pen
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


def key_handler(event):
    """
    Key event handler.

    Add single characters to a list when a key is pressed,
    and remove them from the list when the key is released.
    """
    global text_list
    if event.event_type == KeyEventType.PRESS:
        text_list.append(event.text)
    if event.event_type == KeyEventType.RELEASE:
        text_list.remove(event.text)


def mouse_handler(event):
    """
    Mouse event handler and path creator.

    Remember where the user clicked the mouse, then
    draw a line between the click and release points when the mouse is released."""
    global click_point
    if event.event_type == MouseEventType.PRESS:
        click_point.clear()
        click_point.append(Unit(event.window_pos[0]))
        click_point.append(Unit(event.window_pos[1]))
    if event.event_type == MouseEventType.RELEASE:
        path = Path(click_point, None, "#ff00ff55")
        path.line_to(
            Unit(event.window_pos[0]) - click_point[0],
            Unit(event.window_pos[1]) - click_point[1],
        )


def refresh_func(time: float):
    global text_list
    typing_text.text = " ".join(text_list)


neoscore.setup(display_page_geometry=False)

Path.rect(
    (Mm(-1000000), Mm(-1000000)),
    None,
    Mm(2000000),
    Mm(2000000),
    Brush.no_brush(),
    Pen.no_pen(),
)

click_point = []
text_list = []
typing_text = Text((Unit(250), Unit(250)), None, "begin holding keys down")

neoscore.set_key_event_handler(key_handler)
neoscore.set_mouse_event_handler(mouse_handler)
neoscore.set_viewport_center_pos((Unit(250), Unit(250)))
neoscore.show(
    refresh_func,
    auto_viewport_interaction_enabled=False,
    min_window_size=(500, 500),
    max_window_size=(500, 500),
)
