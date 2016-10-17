#!/usr/bin/env python

from PySide import QtGui
from .point_unit import PointUnit
from .staff_unit import StaffUnit
import abc


class GraphicObject(metaclass=abc.ABCMeta):
    """
    Top level abstract class for a graphical object.
    """
    def __init__(self, parent, scene, x_pos, y_pos):
        """
        Args:
            parent (QGraphicsItem):
            scene (QGraphicsScene):
            x_pos (PointUnit):
            y_pos (PointUnit):
        """
        self.scene = scene
        self.parent = parent
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.scene_space_x_pos = self.x_pos
        self.scene_space_y_pos = self.y_pos
        self.glyph = None

    @property
    def glyph(self):
        """QGraphicsItem: Reference to a Qt QGraphicsItem object responsible for all rendering

        Any modifications made to a staff_object must also be passed to self.glyph"""
        return self._glyph

    @glyph.setter
    def glyph(self, new_glyph):
        # if not isinstance(new_glyph, QtGui.QGraphicsItem):
        #     raise TypeError('glyph must be a QGraphicsItem')
        self._glyph = new_glyph

        # if new_glyph:
        #     # if new_glyph actually contains content (unlike [], for example), push object data to the glyph
        #     self.push_data_to_glyph()

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, new_scene):
        self._scene = new_scene

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        if not (isinstance(new_parent, GraphicObject) or (new_parent is None)):
            raise TypeError('GraphicObject.parent must be a GraphicObject instance or None.')
        self._parent = new_parent

    # @property
    # def children(self):
    #     """list: A list of children Frame or Object instances"""
    #     return self._children
    #
    # @children.setter
    # def children(self, children):
    #     if not (isinstance(children, list) or (children is None)):
    #         raise TypeError('Frame.children must be a list of Frame or Object instances.')
    #     self._children = children

    @property
    def x_pos(self):
        """PointUnit: The frame's X-axis position in relative to its parent.
            If parent is None, position is relative to the scene origin"""
        return self._x_pos

    @x_pos.setter
    def x_pos(self, offset):
        # Enforce conversion to PointUnit
        if isinstance(offset, PointUnit):
            self._x_pos = offset
        elif isinstance(offset, int) or isinstance(offset, float):
            self._x_pos = PointUnit(offset)
        else:
            raise TypeError('GraphicObject.x_pos must be a PointUnit')

    @property
    def y_pos(self):
        """PointUnit: The frame's X-axis position in relative to its parent.
            If parent is None, position is relative to the scene origin"""
        return self._y_pos

    @y_pos.setter
    def y_pos(self, offset):
        # Enforce conversion to PointUnit
        if isinstance(offset, PointUnit):
            self._y_pos = offset
        elif isinstance(offset, int) or isinstance(offset, float):
            self._y_pos = PointUnit(offset)
        else:
            raise TypeError('GraphicObject.y_pos must be a PointUnit')

    @property
    def scene_space_x_pos(self):
        """PointUnit: The object's X-axis position in page space (post-flowable transformation)
            in PointUnit units"""
        return self._paper_space_x_pos

    @scene_space_x_pos.setter
    def scene_space_x_pos(self, offset):
        # Enforce conversion to PointUnit
        if isinstance(offset, PointUnit):
            self._paper_space_x_pos = offset
        elif isinstance(offset, int) or isinstance(offset, float):
            self._paper_space_x_pos = PointUnit(offset)
        else:
            raise TypeError('GraphicObject.scene_space_x_pos must be a PointUnit')

    @property
    def scene_space_y_pos(self):
        """PointUnit: The object's Y-axis position in page space (post-flowable transformation)
            in PointUnit units"""
        return self._paper_space_y_pos

    @scene_space_y_pos.setter
    def scene_space_y_pos(self, offset):
        # Enforce conversion to PointUnit
        if isinstance(offset, PointUnit):
            self._paper_space_y_pos = offset
        elif isinstance(offset, int) or isinstance(offset, float):
            self._paper_space_y_pos = PointUnit(offset)
        else:
            raise TypeError('GraphicObject.scene_space_y_pos must be a PointUnit')

    @abc.abstractmethod
    def build_glyph(self):
        """
        An abstract method that should build a QGraphicsItem, store it in self.glyph, and return it

        Returns: QGraphicsItem
        """
        raise NotImplementedError

    # @property
    # def width(self):
    #     """float: The frame's width in mm."""
    #     return self._width
    #
    # @property
    # def height(self):
    #     """float: The frame's height in mm."""
    #     return self._height

    @property
    def angle(self):
        """float: The frame's angle relative to its parent measured in degrees.
            Positive values turn the frame clockwise while negative values turn counter-clockwise"""
        return self._angle

    @angle.setter
    def angle(self, angle):
        try:
            self._angle = float(angle)
        except ValueError:
            print('Frame.angle must be a number, ignoring setting of angle to "%s"' % str(angle))
            return

    # # Children methods
    # def add_child(self, child):
    #     if not isinstance(child, GraphicObject):
    #         raise TypeError('Call to Frame.add_child() must pass a Frame or Element instance.')
    #     self._children.append(child)

    # Transformation methods -------------------------------

    def translate(self, delta_x=0, delta_y=0):
        """
        Moves this frame relative to its parent by given delta_x and delta_y values

        Args:
            delta_x (float): Positive values translate up, negative values translate down
            delta_y (float): Positive values translate up, negative values translate down

        Returns: None
        """
        if delta_x == 0 and delta_y == 0:
            # If both values are 0, there's nothing to do here. Return.
            return

        # Add delta_x and delta_y to self.x_pos and self.y_pos respectively
        self.x_pos += delta_x
        self.y_pos += delta_y

        # If some modifications to the parent Frame or drawing framework needs to be made, do them here
        return


    def move_to(self, x, y):
        """
        Set this frame's X and Y positions to new values relative to its parent

        Args:
            x (float): New value for x
            y (float): New value for y

        Returns: None
        """
        try:
            self.x_pos = x
            self.y_pos = y
        except ValueError:
            print('In Frame.move_to() both x and y must be numbers, ignoring...')

    def rotate(self, angle):
        """
        Rotate the Frame according to a given angle in degrees

        Args:
            angle (float or int): angle by which to rotate;
                Positive values rotate clockwise, negative values rotate counterclockwise.

        Returns: None
        """
        # Adjust the angle to correct redundant rotation
        if angle < 0:
            adjusted_angle = angle % -360
        else:
            adjusted_angle = angle % 360

        if adjusted_angle == 0:
            # If the passed angle is or adjusts to 0, there is nothing to do here. Return
            return

        ### Method Body ###
        self.angle = adjusted_angle

    def scale(self, x_ratio, y_ratio):
        """
        Args:
            x_ratio (float or int): ratio by which the frame should be scaled along
                its X axis where ``1.0`` is the current size, ``2.0`` would double the size, etc.
                Negative values will mirror the Frame
            y_ratio (float or int): ratio by which the frame should be scaled along
                its Y axis where ``1.0`` is the current size, ``2.0`` would double the size, etc.
                Negative values will mirror the Frame

        Returns: None
        """

        if x_ratio == 0 or y_ratio == 0:
            raise ValueError('In Frame.scale(), neither x_ratio nor y_ratio may be 0.')
        if x_ratio == 1 and y_ratio == 1:
            # If x_ratio and y_ratio are both 1, there is nothing to do. Return
            return


        ### Method Body ###
        pass

    def push_data_to_glyph(self, glyph=None):
        """
        Pushes the contents of this GraphicObject to self.glyph.

        If ``glyph`` is specified, push the contents to that glyph. This is useful for certain special cases
        such as when ``glyph`` is a list of glyphs

        Args:
            glyph(None or QGraphicsItem): Optional target glyph. If omitted (as in most cases), use self.glyph

        """
        if glyph is None:
            target_glyph = self.glyph
        else:
            target_glyph = glyph

        if self.glyph is not None:
            self.glyph.parent = self.parent
            # self.glyph.children = self.children
            self.glyph.scene = self.scene
            self.glyph.setX(self.x_pos)
            self.glyph.setY(self.y_pos)
