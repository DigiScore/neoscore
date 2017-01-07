class Spanner:
    """A Mixin class for GraphicObjects with starting and ending anchors.

    This mixin only provides a common property interface for
    starting and ending anchors. It is up to the concrete object
    to determine how rendering logic should use this information.
    """

    def __init__(self, start, stop):
        """
        Args:
            start (GraphicObject):
            stop (GraphicObject):
        """
        self.start = start
        self.stop = stop
