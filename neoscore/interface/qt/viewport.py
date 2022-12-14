from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QPointF

from neoscore.core.key_event import KeyEventType
from neoscore.core.mouse_event import MouseEventType
from neoscore.interface.qt.converters import (
    q_key_event_to_key_event,
    q_mouse_event_to_mouse_event,
)

_NO_DRAG = 0
_SCROLL_HAND_DRAG = 1
_NO_VIEWPORT_UPDATE = 3
_SCROLL_BAR_AS_NEEDED = 0
_SCROLL_BAR_ALWAYS_OFF = 1
_FOCUS_POLICY_STRONG_FOCUS = 0x1 | 0x2 | 0x8
_FOCUS_POLICY_NO_FOCUS = 0


class Viewport(QtWidgets.QGraphicsView):
    """A QGraphicsView configured for use in interactive neoscore scenes.

    Includes some basic hacky features.
    """

    def __init__(self, scene: QtWidgets.QGraphicsScene):
        super().__init__(scene)
        # Default configs
        self.setViewport(QtWidgets.QOpenGLWidget())
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        # Automatic viewport updates are disabled. Updates are performed
        # manually in the main window refresh function.
        self.set_auto_interaction(True)
        self.setViewportUpdateMode(_NO_VIEWPORT_UPDATE)  # noqa
        self.mouse_event_handler = None
        self.key_event_handler = None

    def set_auto_interaction(self, enabled: bool):
        """Set whether mouse and scrollbar interaction is enabled."""
        self.auto_interaction_enabled = enabled
        if enabled:
            self.setDragMode(_SCROLL_HAND_DRAG)  # noqa
            self.setHorizontalScrollBarPolicy(_SCROLL_BAR_AS_NEEDED)  # noqa
            self.setVerticalScrollBarPolicy(_SCROLL_BAR_AS_NEEDED)  # noqa
        else:
            self.setDragMode(_NO_DRAG)  # noqa
            self.setHorizontalScrollBarPolicy(_SCROLL_BAR_ALWAYS_OFF)  # noqa
            self.setVerticalScrollBarPolicy(_SCROLL_BAR_ALWAYS_OFF)  # noqa

    def wheelEvent(self, event):
        """Implementation of Qt event hook for zooming with the mouse wheel."""
        if not self.auto_interaction_enabled:
            return
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        wheel_delta = event.angleDelta().y()
        # Save the scene pos
        old_pos = self.mapToScene(event.pos())
        # Zoom
        if wheel_delta > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
        self.scale(zoom_factor, zoom_factor)
        # Get the new position
        new_pos = self.mapToScene(event.pos())
        # Move scene to old position
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())

    def scrollContentsBy(self, *args):
        """Override of superclass scroll action to trigger a viewport update."""
        super().scrollContentsBy(*args)
        self.viewport().update()

    def window_document_pos(self) -> QPointF:
        return self.mapToScene(0, 0)

    # Input event handler overrides

    def mouseMoveEvent(self, e):
        if self.mouse_event_handler:
            self.mouse_event_handler(
                q_mouse_event_to_mouse_event(
                    e, MouseEventType.MOVE, self.window_document_pos()
                )
            )
        if self.auto_interaction_enabled:
            super().mouseMoveEvent(e)

    def mousePressEvent(self, e):
        if self.mouse_event_handler:
            self.mouse_event_handler(
                q_mouse_event_to_mouse_event(
                    e, MouseEventType.PRESS, self.window_document_pos()
                )
            )
        if self.auto_interaction_enabled:
            super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        if self.mouse_event_handler:
            self.mouse_event_handler(
                q_mouse_event_to_mouse_event(
                    e, MouseEventType.RELEASE, self.window_document_pos()
                )
            )
        if self.auto_interaction_enabled:
            super().mouseReleaseEvent(e)

    def mouseDoubleClickEvent(self, e):
        if self.mouse_event_handler:
            self.mouse_event_handler(
                q_mouse_event_to_mouse_event(
                    e, MouseEventType.DOUBLE_CLICK, self.window_document_pos()
                )
            )
        if self.auto_interaction_enabled:
            super().mouseDoubleClickEvent(e)

    def keyPressEvent(self, e):
        if self.key_event_handler:
            self.key_event_handler(q_key_event_to_key_event(e, KeyEventType.PRESS))
        if self.auto_interaction_enabled:
            super().keyPressEvent(e)

    def keyReleaseEvent(self, e):
        if self.key_event_handler:
            self.key_event_handler(q_key_event_to_key_event(e, KeyEventType.RELEASE))
        if self.auto_interaction_enabled:
            super().keyPressEvent(e)

    # End of input event handler overrides
