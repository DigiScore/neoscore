from brown.core.path_element_type import PathElementType
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
            element_type (PathElementType or int enum value):
                The type of element this represents.

        Raises:
            ValueError:
        """
        self.qt_object = qt_object
        self._parent_path = parent_path
        self._index = index
        self._pos = Point(GraphicUnit(qt_object.x), GraphicUnit(qt_object.y))
        self._element_type = (
            element_type
            if isinstance(element_type, PathElementType)
            else PathElementType(element_type)
        )

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self):
        return self._pos

    @property
    def path_interface(self):
        """PathInterface: The path interface this element belongs in."""
        return self._parent_path

    @property
    def index(self):
        """int: The index of this element in the parent path"""
        return self._index

    @property
    def element_type(self):
        """PathElementType: The type of this element.

        This has a 1:1 correspondence with `PathElement.element_type`.
        """
        # TODO LOW: This is not accurate. When creating a curve, Qt
        # marks the first control point as being a CurveToElement, and
        # all following as CurveToDataElement's--- need to work around
        # this so that the control points are clearly marked
        # differently from the end point.
        return self._element_type
