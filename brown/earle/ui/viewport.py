from PyQt5 import QtGui, QtWidgets


class Viewport(QtWidgets.QGraphicsView):
    """The graphical view and working area.

    Includes some basic hacky interactivity features,
    architecture will need to be revisited once a general
    input processing system is worked out.
    """

    def __init__(self, scene):
        """
        Args:
            scene (QGraphicsScene):
        """
        super().__init__(scene)
        # Default configs
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setDragMode(1)  # ScrollHandDrag

    def wheelEvent(self, event):
        """Zoom in or out of the view."""

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
