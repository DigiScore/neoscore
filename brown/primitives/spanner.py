from brown.utils.anchored_point import AnchoredPoint


class Spanner:
    """A Mixin class for GraphicObjects with starting and ending anchors.

    This mixin only provides a common property interface for
    starting and ending anchors. It is up to the concrete object
    to determine how rendering logic should use this information.
    """

    def __init__(self, start, stop):
        """
        Args:
            start (AnchoredPoint or tuple init args):
            stop (AnchoredPoint or tuple init args):
        """
        if isinstance(start, tuple):
            start = AnchoredPoint(*start)
        if start.parent is None:
            start.parent = self
        if isinstance(stop, tuple):
            stop = AnchoredPoint(*stop)
        if stop.parent is None:
            stop.parent = self
        self.start = start
        self.stop = stop
