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
        """Generate automatic layout controllers.

        The generated controllers are stored in `self.auto_layout_controllers`
        in sorted order according to ascending x position

        Warning:
            This overwrites the contents of self.auto_layout_controllers

        Returns: None
        """
        self.auto_layout_controllers = []
        live_page_width = brown.document.paper.live_width * units.mm
        live_page_height = brown.document.paper.live_height * units.mm
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
            x (float): x coordinate in pixels
            y (float): y coordinate in pixels

        Returns: tuple(float: x, float: y) coordinates in pixels
        """
        # Seek to the page and line-on-page based on auto layout controllers
        self._generate_auto_layout_controllers()
        page_num = 1
        line_on_page = 1
        current_x_offset = self.x
        current_y_offset = self.y
        remaining_x = x
        for controller in self.auto_layout_controllers:
            if controller.x > x:
                break
            remaining_x -= ((brown.document.paper.live_width * units.mm) -
                            current_x_offset)
            if isinstance(controller, AutoLineBreak):
                line_on_page += 1
                current_x_offset = 0
                current_y_offset += self.height + controller.margin_above_next
            elif isinstance(controller, AutoPageBreak):
                page_num += 1
                line_on_page = 1
                current_x_offset = 0
                current_y_offset = controller.margin_above_next
        print('remaining x is', remaining_x)
        print('page num is ', page_num)
        print('line on page is ', line_on_page)
        page_x, page_y = brown.document._page_origin_in_doc_space(page_num)
        print('page coords: ', page_x, page_y)
        line_x = page_x + current_x_offset
        line_y = page_y + current_y_offset
        print('line coords: ', line_x, line_y)
        return line_x + remaining_x, line_y + y
