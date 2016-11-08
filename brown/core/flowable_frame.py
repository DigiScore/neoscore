from brown.utils import units


class FlowableFrame:

    def __init__(self, x, y, document, width, height, default_span_width=None):
        self.x = x
        self.y = y
        self.document = document
        self.width = width
        self.height = height
        if default_span_width:
            self._default_span_width = default_span_width
        else:
             # TODO: compute default from document
            self._default_span_width = units.inch * 6.5

    ######## PUBLIC PROPERTIES ########

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, value):
        self._document = value

    ######## PRIVATE METHODS ########

    def _span_width_at(self, x):
        """float: The frame width at a given x coordinate."""
        # TODO: Implement variable width frames later
        return self._default_span_width

    def _local_space_to_doc_space(self, x, y):
        """Convert a position inside the frame to its position in the document.

        Args:
            x (float): x coordinate
            y (float): y coordinate

        Returns: tuple(float: x, float: y)
        """
        # TODO: WIP
        doc_x = x % self._default_span_width
        return doc_x, 9999999999  # Very wip
