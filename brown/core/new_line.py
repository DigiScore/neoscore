from brown.core import brown
from brown.core.layout_controller import LayoutController
from brown.utils.point import Point


class NewLine(LayoutController):
    """A line break controller."""

    def __init__(self, flowable_frame, x, page_number, page_pos, offset_y=0):
        """
        Args:
            flowable_frame (FlowableFrame): The parent frame.
            x (float): The x position in pixels in the frame's local space.
            page_number (int): The page number
            page_pos (Point): The page position of the top left corner of this line.
            offset_y (float): The space between the bottom of the
                current line and the top of the next, in pixels.

        TODO: Priority low - page_number and page_pos in signature are
              in swapped order compare to Document._page_pos_to_doc signature.
              Something should change so all use the same order.
        """
        super().__init__(flowable_frame, x)
        self._page_pos = Point(page_pos)
        self._page_number = page_number
        self.offset_y = offset_y

    ######## PUBLIC PROPERTIES ########

    @property
    def offset_y(self):
        """float: The space in pixels before the next line."""
        return self._offset_y

    @offset_y.setter
    def offset_y(self, value):
        self._offset_y = value

    @property
    def page_number(self):
        """int: The page number"""
        return self._page_number

    @property
    def page_pos(self):
        """Point: The page position of the top left corner of this line."""
        return self._page_pos

    @property
    def doc_start_pos(self):
        """Point: The position of the new line's top left corner in doc space

        This property is read-only
        """
        return brown.document._page_pos_to_doc(self.page_pos, self.page_number)

    @property
    def doc_end_pos(self):
        """Point: The position of the new line's bottom right corner in doc space

        This property is read-only
        """
        return self.doc_start_pos + Point(self.length, self.height)

    @property
    def length(self):
        """Unit: The length of the line.

        This property is read-only.
        """
        # TODO: When breaks are made more flexible this needs to be updated.
        return brown.document.paper.live_width - self.page_pos.x

    @property
    def height(self):
        """Unit: The height of the line.

        This property is read-only.
        """
        # TODO: When breaks are made more flexible this needs to be updated.
        return self.flowable_frame.height

    ######## PRIVATE PROPERTIES ########

    @property
    def _is_automatic(self):
        return False
