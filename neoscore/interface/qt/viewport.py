from PyQt5 import QtGui, QtWidgets

_SCROLL_HAND_DRAG = 1
_NO_VIEWPORT_UPDATE = 3


class Viewport(QtWidgets.QGraphicsView):
    """A QGraphicsView configured for use in interactive neoscore scenes.

    Includes some basic hacky features.
    """

    def __init__(self, scene: QtWidgets.QGraphicsScene):
        super().__init__(scene)
        # Default configs
        self.setViewport(QtWidgets.QOpenGLWidget())
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setDragMode(_SCROLL_HAND_DRAG)  # noqa
        # Automatic viewport updates are disabled. Updates are performed
        # manually in the main window refresh function.
        self.setViewportUpdateMode(_NO_VIEWPORT_UPDATE)  # noqa

    def wheelEvent(self, event):
        """Implementation of Qt event hook for zooming with the mouse wheel."""
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
