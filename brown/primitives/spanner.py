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
        self.start = AnchoredPoint(start)
        self.stop = AnchoredPoint(stop)
