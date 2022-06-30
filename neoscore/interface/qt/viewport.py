from PyQt5 import QtGui, QtWidgets

_NO_DRAG = 0
_SCROLL_HAND_DRAG = 1
_NO_VIEWPORT_UPDATE = 3
_SCROLL_BAR_AS_NEEDED = 0
_SCROLL_BAR_ALWAYS_OFF = 1


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

    def set_auto_interaction(self, enabled: bool):
        """Set whether mouse and scrollbar interaction is enabled."""
        self.mouse_interaction_enabled = enabled
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
        if not self.mouse_interaction_enabled:
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
