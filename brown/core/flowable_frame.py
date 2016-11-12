from brown.utils import units
from brown.core import brown
from brown.core.layout_controller import LayoutController
from brown.core.auto_line_break import AutoLineBreak
from brown.core.auto_page_break import AutoPageBreak


class FlowableFrame:

    def __init__(self, x, y, width, height, y_padding=None):
        """
        Args:
            x (float): Starting x position in pixels relative to
                the top left corner of the live document area on the first page
            y (float): Starting y position in pixels relative to
                the top left corner of the live document area on the first page
            width (float): width of the frame in pixels
            height (float): height of the frame in pixels
            y_padding (float): The min gap between frame sections in pixels
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if y_padding is None:
            self.y_padding = units.mm * 20
        else:
            self.y_padding = y_padding

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
    def y_padding(self):
        return self._y_padding

    @y_padding.setter
    def y_padding(self, value):
        self._y_padding = value

    @property
    def layout_controllers(self):
        """list[LayoutController]: Explicit controllers for layout

        Layout support for explicit controllers not yet supported.
        """
        return self._layout_controllers

    @layout_controllers.setter
    def layout_controllers(self, value):
        if (not isinstance(value, list) or
                not all(isinstance(c, LayoutController) for c in value)):
            # TODO: Maybe remove type guards?
            raise TypeError
        self._layout_controllers = value

    @property
    def auto_layout_controllers(self):
        """list[LayoutController]: Auto-generated controllers for layout"""
        return self._auto_layout_controllers

    @auto_layout_controllers.setter
    def auto_layout_controllers(self, value):
        if (not isinstance(value, list) or
                not all(isinstance(c, LayoutController) for c in value)):
            # TODO: Maybe remove type guards?
            raise TypeError
        self._auto_layout_controllers = value

    ######## PRIVATE METHODS ########

    def _generate_auto_layout_controllers(self):
        """
        Generate automatic layout controllers.

        Warning:
            This overwrites the contents of self.auto_layout_controllers

        Returns: None
        """
        self.auto_layout_controllers = []
        live_page_width = brown.paper.live_width * units.mm
        live_page_height = brown.paper.live_height * units.mm
        # The progress the layout generation has reached along the frame's width.
        # When the entire flowable has been covered, this value will == self.width
        x_progress = 0
        # Current position on the page relative to the top left corner of the live page area
        current_page_x = self.x
        current_page_y = self.y
        while True:
            delta_x = live_page_width - current_page_x
            x_progress += delta_x
            current_page_y = current_page_y + self.height + self.y_padding
            if x_progress >= self.width:
                break
            if current_page_y > live_page_height:
                self.auto_layout_controllers.append(
                    AutoPageBreak(self, x_progress, self.y_padding))
                current_page_y = 0
            else:
                self.auto_layout_controllers.append(
                    AutoLineBreak(self, x_progress, 0))
                current_page_x = 0

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
