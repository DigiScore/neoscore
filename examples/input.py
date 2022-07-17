"""
This example demonstrates basic mouse and keyboard input
in the interactive runtime viewport.
"""

from neoscore.core import neoscore
from neoscore.core.rich_text import RichText
from neoscore.core.units import Mm

neoscore.setup()


annotation = """
<p>
Neoscore has basic support for monitoring keyboard and mouse input. This example
listens for events and simply prints them to the console, but the same handlers used
here can be used to implement more sophisticated interactions.
</p>
<p>
When using mouse event handlers and keyboard arrow key handlers, you may want to consider disabling automatic viewport interaction.
</p>
"""
RichText((Mm(1), Mm(1)), None, annotation, width=Mm(120))


def mouse_handler(event):
    """Simply print mouse events.

    Since every mouse movement fires an event, this generate a lot of logs.
    """
    print(event)


def key_handler(event):
    """Simply print key events"""
    print(event)


neoscore.set_mouse_event_handler(mouse_handler)
neoscore.set_key_event_handler(key_handler)


if __name__ == "__main__":
    neoscore.show(auto_viewport_interaction_enabled=False)
