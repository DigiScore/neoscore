from brown.utils.point import Point
from brown.core import brown
from brown.utils.mm import Mm
from brown.core.layout_controller import LayoutController
from brown.core.auto_new_line import AutoNewLine
from brown.core.auto_new_page import AutoNewPage


class FlowableFrame:

    def __init__(self, pos, width, height, y_padding=None):
        """
        Args:
            pos (Point or tuple): Starting position in relative to
                the top left corner of the live document area of the first page
            width (GraphicUnit): width of the frame
            height (GraphicUnit): height of the frame
            y_padding (GraphicUnit): The min gap between frame sections
        """
        self.pos = Point(pos)
        self.width = width
        self.height = height
        if y_padding is None:
            self.y_padding = Mm(20)
        else:
            self.y_padding = y_padding

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self):
        """Point: The starting point of the frame on the first page."""
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    @property
    def x(self):
        """GraphicUnit:"""
        return self.pos.x

    @x.setter
    def x(self, value):
        self.pos.x = value

    @property
    def y(self):
        """GraphicUnit:"""
        return self.pos.y

    @y.setter
    def y(self, value):
        self.pos.y = value

    @property
    def width(self):
        """GraphicUnit:"""
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """GraphicUnit:"""
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def y_padding(self):
        """GraphicUnit:"""
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
        live_page_width = brown.document.paper.live_width
        live_page_height = brown.document.paper.live_height
        # The progress the layout generation has reached along the frame's width.
        # When the entire flowable has been covered, this value will == self.width
        x_progress = Mm(0)
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
                    AutoNewPage(self, x_progress))
                current_page_y = Mm(0)
            else:
                self.auto_layout_controllers.append(
                    AutoNewLine(self, x_progress, self.y_padding))
                current_page_x = Mm(0)

    def _local_space_to_doc_space(self, point):
        """Convert a position inside the frame to its position in the document.

        Coordinates relative to the top left corner of the first page.

        Args:
            local_point (tuple or Point): An x-y coordinate in flowable space

        Returns:
            Point: An x-y coordinate in document space
        """
        local_point = Point(point)
        # Seek to the page and line-on-page based on auto layout controllers
        self._generate_auto_layout_controllers()
        page_num = 1
        line_on_page = 1
        current_x_offset = self.x  # Offsets relative to ideal line start
        current_y_offset = self.y  # on left margin
        remaining_x = local_point.x
        # Calculate position relative to the top left corner of the live page
        # area of the current page
        for controller in self.auto_layout_controllers:
            if controller.x > local_point.x:
                break
            remaining_x -= (brown.document.paper.live_width -
                            current_x_offset)
            if isinstance(controller, AutoNewLine):
                line_on_page += 1
                current_x_offset = Mm(0)
                current_y_offset += self.height + controller.offset_y
            elif isinstance(controller, AutoNewPage):
                page_num += 1
                line_on_page = 1
                current_x_offset = Mm(0)
                current_y_offset = controller.offset_y
                print('current_y_offset changed to', current_y_offset)
        # Locate current page origin in doc space and apply offsets
        print('remaining x is', remaining_x)
        print('page num is ', page_num)
        print('line on page is ', line_on_page)
        page_x, page_y = brown.document._page_origin_in_doc_space(page_num)
        print('page coords: ', page_x, page_y)
        line_x = page_x + current_x_offset
        line_y = page_y + current_y_offset
        print('line coords: ', line_x, line_y)
        print('local point y: ', local_point.y)
        return Point(line_x + remaining_x, line_y + local_point.y)
