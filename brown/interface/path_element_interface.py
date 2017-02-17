from brown.utils.path_element_type import PathElementType
from brown.utils.point import Point
from brown.utils.units import GraphicUnit


class PathElementInterface:

    """An element of a path or subpath.

    Becuase QPainterPath::Element instances can't be directly created,
    to instantiate an instance of this class you should query the parent
    PathInterface.elements[-1] after creating an element, and pass its
    result to the constructor here.
    """

    def __init__(self, qt_object, parent_path, index, element_type):
        """
        Args:
            qt_object (QtGui.Element): The Qt object this element refers to
            parent_path (PathInterface): The path this element belongs to
            index (int): The position of this element in the parent path.
            element_type (int): The type of element this represents. If None,
                this will attempt to guess the type. Type guessing for move_to
                and line_to elements is guaranteed to be accurate, but
                for distinguishing curves and control points is unsafe and
                will throw a ValueError

        Raises:
            ValueError:
        """
        self._qt_object = qt_object
        self._parent_path = parent_path
        self._index = index
        self._pos = Point(qt_object.x, qt_object.y).to_unit(GraphicUnit)
        self._pos.setters_hook = self._update_element_in_parent_path
        if isinstance(element_type, int):
            # TODO: Clean up this logic
            self._element_type = PathElementType(element_type)
        elif isinstance(element_type, PathElementType):
            self._element_type = element_type
        else:
            raise TypeError

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._pos.setters_hook = self._update_element_in_parent_path
        self._update_element_in_parent_path()

    @property
    def parent_path(self):
        """PathInterface: The path this element belongs to.

        This property is read-only."""
        return self._parent_path

    @property
    def index(self):
        """int: The position of this element in the parent path"""
        return self._index

    @property
    def element_type(self):
        """PathElementType: Enumeration for the type of element.

        This value is read-only.
        """
        # TODO: This is not accurate.
        #       When creating a curve, Qt marks the first control point
        #       as being a CurveToElement, and all following as
        #       CurveToDataElement's--- need to work around this so that
        #       the control points are clearly marked differently from the
        #       end point.
        return self._element_type

    ######## PRIVATE PROPERTIES ########

    def _update_element_in_parent_path(self):
        """Push element properties to self._qt_object and the parent path

        Returns: None
        """
        self.parent_path.set_element_position_at(self.index, self.pos)
        self.parent_path._update_qt_object_path()
