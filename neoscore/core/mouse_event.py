from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple


class MouseButton(Enum):
    """Enum for mouse buttons.

    This currently only supports left, middle, and right buttons.

    The enum integer values are arbitrary and may change in the future.
    """

    LEFT = auto()
    MIDDLE = auto()
    RIGHT = auto()


class MouseEventType(Enum):
    """Enum for mouse event types.

    The enum integer values are arbitrary and may change in the future.
    """

    MOVE = auto()
    """The mouse was moved while a button was held"""

    PRESS = auto()
    """A mouse button was pressed"""

    RELEASE = auto()
    """A mouse button was released"""

    DOUBLE_CLICK = auto()
    """A mouse button was double clicked"""


@dataclass(frozen=True)
class MouseEvent:
    """A mouse input event."""

    event_type: MouseEventType
    """The type of the event"""

    button: Optional[MouseButton]
    """The button pressed, if any.

    For mouse move events, this is the button pressed down while moving. For press and
    double click events, this is the button that caused the event. For release events,
    this is ``None``.
    
    Mouse events with multiple simultaneous button presses will somewhat arbitrarily
    return the first button pressed in order left, right, then middle.
    """

    window_pos: Tuple[int, int]
    """The mouse position on the window in ``x, y`` pixels."""
