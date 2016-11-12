from brown.utils.paper_templates import paper_templates


class Paper:

    def __init__(self, width, height,
                 margin_top, margin_right,
                 margin_bottom, margin_left,
                 gutter=0):
        self.width = width
        self.height = height
        self.margin_top = margin_top
        self.margin_right = margin_right
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.gutter = gutter

    ######## CLASS METHODS ########

    @classmethod
    def from_template(cls, template):
        """Construct a Paper object from a set of pre-configured paper types.

        Args:
            template (str): Name of the Paper template (case-insensitive)

        Currently supported paper types are 'A4'.
        """
        try:
            return cls(*paper_templates[template.upper()])
        except KeyError:
            raise KeyError('Paper template {} not supported'.format(template))

    ######## PUBLIC PROPERTIES ########

    @property
    def width(self):
        """float: The page width in mm"""
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """float: The page height in mm"""
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def margin_top(self):
        """float: The top margin in mm"""
        return self._margin_top

    @margin_top.setter
    def margin_top(self, value):
        self._margin_top = value

    @property
    def margin_right(self):
        """float: The right margin in mm"""
        return self._margin_right

    @margin_right.setter
    def margin_right(self, value):
        self._margin_right = value

    @property
    def margin_bottom(self):
        """float: The bottom margin in mm"""
        return self._margin_bottom

    @margin_bottom.setter
    def margin_bottom(self, value):
        self._margin_bottom = value

    @property
    def margin_left(self):
        """float: The left margin in mm"""
        return self._margin_left

    @margin_left.setter
    def margin_left(self, value):
        self._margin_left = value

    @property
    def gutter(self):
        """float: The page gutter in mm"""
        return self._gutter

    @gutter.setter
    def gutter(self, value):
        self._gutter = value

    @property
    def live_width(self):
        return (self.width - self.gutter -
                self.margin_left - self.margin_right)

    @property
    def live_height(self):
        return self.height - self.margin_bottom - self.margin_top
