from brown.utils.point import Point
from brown.core import brown
from brown.utils.units import Mm, Unit
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

        TODO: Keep the results of this computation so it only has to be
              performed when the auto layout controllers might have changed.
        """
        self.auto_layout_controllers = []
        live_page_width = brown.document.paper.live_width
        live_page_height = brown.document.paper.live_height
        # The progress the layout generation has reached along the frame's width.
        # When the entire flowable has been covered, this value will == self.width
        x_progress = Mm(0)
        # Current position on the page relative to the top left corner
        # of the live page area
        pos_on_page = Point(self.pos)
        page_number = 1
        while True:
            delta_x = live_page_width - pos_on_page.x
            x_progress += delta_x
            pos_on_page.y = pos_on_page.y + self.height + self.y_padding
            if x_progress >= self.width:
                break
            if pos_on_page.y > live_page_height:
                pos_on_page.y = Mm(0)
                page_number += 1
                doc_pos = brown.document._page_pos_to_doc(pos_on_page, page_number)
                self.auto_layout_controllers.append(
                    AutoNewPage(self, x_progress, doc_pos))
            else:
                pos_on_page.x = Mm(0)
                doc_pos = brown.document._page_pos_to_doc(pos_on_page, page_number)
                self.auto_layout_controllers.append(
                    AutoNewLine(self, x_progress, doc_pos, self.y_padding))

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
        # Current position on the page relative to the top left corner
        # of the live page area
        pos_on_page = Point(self.pos)
        remaining_x = local_point.x
        # Calculate position relative to the top left corner of the live page
        # area of the current page
        for controller in self.auto_layout_controllers:
            if controller.x > local_point.x:
                break
            remaining_x -= (brown.document.paper.live_width -
                            pos_on_page.x)
            if isinstance(controller, AutoNewLine):
                pos_on_page.x = Mm(0)
                pos_on_page.y += self.height + controller.offset_y
            elif isinstance(controller, AutoNewPage):
                page_num += 1
                pos_on_page.x = Mm(0)
                pos_on_page.y = controller.offset_y
                # print('pos_on_page.y changed to', pos_on_page.y)
        # Locate current page origin in doc space and apply offsets
        # print('remaining x is', remaining_x)
        # print('page num is ', page_num)
        page_x, page_y = brown.document._page_origin_in_doc_space(page_num)
        # print('page coords: ', page_x, page_y)
        line_x = page_x + pos_on_page.x
        line_y = page_y + pos_on_page.y
        # print('line coords: ', line_x, line_y)
        # print('local point y: ', local_point.y)
        return Point(line_x + remaining_x, line_y + local_point.y)

    def _x_pos_rel_to_line_start(self, x):
        """Find the distance of an x-pos to the left edge of its laid-out line.

        Args:
            x (Unit): The local x coordinate.

        Returns: Unit
        """
        # Seek to the page and line-on-page based on auto layout controllers
        self._generate_auto_layout_controllers()
        current_x_offset = self.x  # Offsets relative to ideal line start
        remaining_x = x
        # Calculate position relative to the top left corner of the live page
        # area of the current page
        for controller in self.auto_layout_controllers:
            if controller.x > x:
                break
            remaining_x -= (brown.document.paper.live_width -
                            current_x_offset)
            if isinstance(controller, AutoNewLine):
                current_x_offset = Mm(0)
            elif isinstance(controller, AutoNewPage):
                current_x_offset = Mm(0)
                # print('current_y_offset changed to', current_y_offset)
        return remaining_x

    def _x_pos_rel_to_line_end(self, x):
        """Find the distance of an x-pos to the right edge of its laid-out line.

        Args:
            x (Unit): The local x coordinate.

        Returns: Unit
        """
        return (self._x_pos_rel_to_line_start(x) -
                brown.document.paper.live_width)
