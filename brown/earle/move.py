from brown.earle.command import Command


class Move(Command):

    """Move a collection of `GraphicObject`s"""

    def __init__(self, receiver, dx, dy):
        """
        Args:
            receiver (list[GraphicObject]): The collection of objects to move.
                No objects in this collection should be parents of each other,
                or weird behavior will occur.
            dx (Unit): The x-axis delta
            dy (Unit): The y-axis delta
        """
        self._receiver = receiver
        self._dx = dx
        self._dy = dy

    @property
    def dx(self):
        """Unit: The x-axis delta"""
        return self._dx

    @property
    def dy(self):
        """Unit: The y-axis delta"""
        return self._dy

    def execute(self):
        for grob in self.receiver:
            grob.x += self.dx
            grob.y += self.dy

    def undo(self):
        for grob in self.receiver:
            grob.x -= self.dx
            grob.y -= self.dy
