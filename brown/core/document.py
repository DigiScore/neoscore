from brown.config import config
from brown.utils.point import Point
from brown.core.paper import Paper
from brown.utils.units import Mm, GraphicUnit
from brown.core.graphic_object import GraphicObject


class Document(GraphicObject):

    """A pseudo-object representing the document origin."""

    def __init__(self, paper=None):
        if paper is None:
            try:
                self.paper = Paper.from_template(config.DEFAULT_PAPER_TYPE)
            except KeyError:
                raise config.InvalidConfigError(
                    'DEFAULT_PAPER_TYPE of {} is not supported'.format(
                        config.DEFAULT_PAPER_TYPE))
        else:
            self.paper = paper
        GraphicObject.__init__(self, (GraphicUnit(0), GraphicUnit(0)))

    ######## PUBLIC PROPERTIES ########

    @property
    def paper(self):
        """Paper: The paper type of the document"""
        return self._paper

    @paper.setter
    def paper(self, value):
        self._paper = value

    @property
    def parent(self):
        """None: By definition, a document has no parent.

        This property exists only as an override of the GraphicObject
        to prevent attempts to register the document with itself.
        """
        return None

    @parent.setter
    def parent(self, value):
        # Override parent setter to do nothing since,
        # by definition, a document has no parent
        pass

    ######## PRIVATE PROPERTIES ########

    @property
    def _page_display_gap(self):
        """float: The visual horizontal gap between pages, in pixels."""
        return Mm(15)

    ######## PRIVATE METHODS ########

    def _page_origin_in_doc_space(self, page_number):
        """Find the position of the origin of the live page area.

        The origin is the top left corner of the live area, equivalent to
        the real page corner plus margins and gutter.

        Args:
            page_number (int): The number of the page to locate

        Returns:
            Point: The position of the origin of the given page.
        """
        if page_number < 1:
            raise ValueError('page_number must be 1 or greater.')
        # Left edge of paper (not including margin/gutter)
        x_page_left = ((self.paper.width + self._page_display_gap) *
                       (page_number - 1))
        x_page_origin = x_page_left + self.paper.margin_left
        y_page_origin = self.paper.margin_top
        return Point(x_page_origin, y_page_origin)

    def _page_pos_to_doc(self, pos, page_number):
        """Take a position on a page number and find its doc-space position

        The origin is the top left corner of the live area, equivalent to
        the real page corner plus margins and gutter.

        Args:
            pos (Point): The position relative to the origin of the
                live page area

        Returns:
            Point: A document-space position
        """
        return pos + self._page_origin_in_doc_space(page_number)

    ######## PUBLIC METHODS ########

    def render(self):
        """Render all items in the document.

        Returns: None
        """
        for child in self.children:
            child.render()
