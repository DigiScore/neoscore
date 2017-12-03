from brown.interface.paper_interface import PaperInterface
from brown.utils.paper_templates import paper_templates


class Paper:

    """A description of a type of paper to base `Page`s on."""

    def __init__(self, width, height,
                 margin_top, margin_right,
                 margin_bottom, margin_left,
                 gutter=None):
        """
        Args:
            width (Unit): The paper width.
            height (Unit): The paper height.
            margin_top (Unit): The paper top margin.
            margin_right (Unit): The paper right margin.
            margin_bottom (Unit): The paper bottom margin.
            margin_left (Unit): The paper left margin.
            gutter (Unit): The paper gutter.
        """
        self._width = width
        self._height = height
        self._margin_top = margin_top
        self._margin_right = margin_right
        self._margin_bottom = margin_bottom
        self._margin_left = margin_left
        self._gutter = gutter

    ######## CLASS METHODS ########

    @classmethod
    def from_template(cls, template):
        """Construct a Paper object from a set of pre-configured paper types.

        Args:
            template (str): Name of the Paper template (case-sensitive)

        Returns: Paper
        """
        try:
            return cls(*paper_templates[template])
        except KeyError:
            raise KeyError('Paper template {} not supported'.format(template))

    ######## PUBLIC PROPERTIES ########

    @property
    def width(self):
        """Unit: The page width"""
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """Unit: The page height"""
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def margin_top(self):
        """Unit: The top margin"""
        return self._margin_top

    @margin_top.setter
    def margin_top(self, value):
        self._margin_top = value

    @property
    def margin_right(self):
        """Unit: The right margin"""
        return self._margin_right

    @margin_right.setter
    def margin_right(self, value):
        self._margin_right = value

    @property
    def margin_bottom(self):
        """Unit: The bottom margin"""
        return self._margin_bottom

    @margin_bottom.setter
    def margin_bottom(self, value):
        self._margin_bottom = value

    @property
    def margin_left(self):
        """Unit: The left margin"""
        return self._margin_left

    @margin_left.setter
    def margin_left(self, value):
        self._margin_left = value

    @property
    def gutter(self):
        """Unit: The page gutter.

        TODO: Gutter support is not fully implemented.
        """
        return self._gutter

    @gutter.setter
    def gutter(self, value):
        self._gutter = value

    @property
    def live_width(self):
        """The printable width of the page"""
        return (self.width - self.gutter -
                self.margin_left - self.margin_right)

    @property
    def live_height(self):
        """The printable height of the page"""
        return self.height - self.margin_bottom - self.margin_top

    ######## SPECIAL METHODS ########

    def __repr__(self):
        return '{}({}, {}, {}, {}, {}, {}, {})'.format(
            type(self).__name__,
            self.width, self.height,
            self.margin_top, self.margin_right,
            self.margin_bottom, self.margin_left,
            self.gutter)

    def __hash__(self):
        return hash((
            self.__class__,
            self.width, self.height,
            self.margin_top, self.margin_right,
            self.margin_bottom, self.margin_left,
            self.gutter))

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.width == other.width
                and self.height == other.height
                and self.margin_top == other.margin_top
                and self.margin_right == other.margin_right
                and self.margin_bottom == other.margin_bottom
                and self.margin_left == other.margin_left
                and self.gutter == other.gutter)

    ######## PUBLIC METHODS ########

    def make_rotation(self):
        """Create a 90 degree clockwise rotation of this `Paper`.

        The `gutter` field is not changed in this new `Paper`.

        Returns: Paper
        """
        return Paper(
            self.height,
            self.width,
            self.margin_left,
            self.margin_top,
            self.margin_right,
            self.margin_bottom,
            self.gutter)

    ######## PRIVATE METHODS ########

    def _to_interface(self):
        """Construct and return a PaperInterface based on this Paper.

        Returns: PaperInterface
        """
        return PaperInterface(self)
