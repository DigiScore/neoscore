#!/usr/bin/env python

from PySide.QtGui import QGraphicsView
from PySide.QtCore import QPoint
from PySide.QtCore import Qt


class TestingView(QGraphicsView):
    def __init__(self, *args, **kwargs):

        QGraphicsView.__init__(self, *args, **kwargs)
        # self.setAlignment(Qt.AlignCenter)
        # self._last_mouse_pos = None  # Awful terrible way of handling delta mouse movement

    def wheelEvent(self, event):
        """
        Zoom in or out of the view.
        """
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor
        wheel_delta = event.delta()

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        if wheel_delta > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())
