#!/usr/bin/env python

from .document import Document
# from .line_break import LineBreak
from .exceptions import PointOutsideSectionError
from .flowable_section import FlowableSection
from .page import Page
from .paper import Paper
from .point_unit import PointUnit


class Flowable:
    """
    A flowable container for an arbitrary number of GraphicObjects which handles wrapping and translates object 
        coordinates into scene-space coordinates.
    
    The Flowable is designed as a single long rectangle. Child GraphicObjects query the Flowable to
    determine their scene-space coordinates.
    """
    def __init__(self, document, starting_scene_pos_x, starting_scene_pos_y, length, height,
                 default_vertical_padding=36):
        """
        Args:
            document (Document):
            starting_scene_pos_x (PointUnit or int or float): Starting scene x position
            starting_scene_pos_y (PointUnit or int or float): Starting scene y position
            length (PointUnit or int or float): Length of the container
            height (PointUnit or int or float): Height of the container
            default_vertical_padding (PointUnit or int or float): Default padding to be added between
                systems after line breaks
        """
        self.document = document
        self.starting_scene_pos_x = starting_scene_pos_x
        self.starting_scene_pos_y = starting_scene_pos_y
        self.length = length
        self.height = height
        self.default_vertical_padding = default_vertical_padding
        self._section_list = []

    @property
    def document(self):
        """Document: The document containing this Flowable. Internally, page information is taken from this."""
        return self._document
    
    @document.setter
    def document(self, new_value):
        if not isinstance(new_value, Document):
            raise TypeError
        self._document = new_value
    
    @property
    def starting_page(self):
        """Page: The page where this Flowable begins"""
        return self.document.page_of_coordinate(self.starting_scene_pos_x, self.starting_scene_pos_y)
        
    @property
    def starting_scene_pos_x(self):
        """PointUnit: The starting x position (in scene-space) of this Flowable"""
        return self._starting_scene_pos_x
    
    @starting_scene_pos_x.setter
    def starting_scene_pos_x(self, new_value):
        self._starting_scene_pos_x = PointUnit(new_value)
        
    @property
    def starting_scene_pos_y(self):
        """PointUnit: The starting y position (in scene-space) of this Flowable"""
        return self._starting_scene_pos_y
    
    @starting_scene_pos_y.setter
    def starting_scene_pos_y(self, new_value):
        self._starting_scene_pos_y = PointUnit(new_value)
        
    @property
    def length(self):
        """PointUnit: The length of this Flowable"""
        return self._length
    
    @length.setter
    def length(self, new_value):
        self._length = PointUnit(new_value)
        
    @property
    def height(self):
        """PointUnit: The height of this Flowable"""
        return self._height
    
    @height.setter
    def height(self, new_value):
        self._height = PointUnit(new_value)

    @property
    def default_vertical_padding(self):
        """PointUnit: The default space to add between lines after line breaks"""
        return self._default_vertical_padding

    @default_vertical_padding.setter
    def default_vertical_padding(self, new_value):
        self._default_vertical_padding = PointUnit(new_value)
        
    # @property
    # def line_break_list(self):
    #     """list[LineBreak]: A list of LineBreak objects in the Flowable"""
    #     return self._line_break_list
    # 
    # @line_break_list.setter
    # def line_break_list(self, new_value):
    #     if isinstance(new_value, list):
    #         for item in new_value:
    #             if not isinstance(new_value, LineBreak):
    #                 raise TypeError
    #     elif isinstance(new_value, LineBreak):
    #         new_value = [new_value]
    #     else:
    #         raise TypeError
    #     self._line_break_list = new_value
    
    @property
    def section_list(self):
        """list[FlowableSection]: A list of FlowableSection objects in the Flowable"""
        return self._section_list
    
    # @section_list.setter
    # def section_list(self, new_value):
    #     if isinstance(new_value, list):
    #         for item in new_value:
    #             if not isinstance(new_value, FlowableSection):
    #                 raise TypeError
    #     elif isinstance(new_value, FlowableSection):
    #         new_value = [new_value]
    #     else:
    #         raise TypeError
    #     self._section_list = new_value

    def section_at_flowable_space_coord(self, x_pos):
        """
        Find which FlowableSection in ``self.section_list`` contains a given flowable space x coordinate

        Args:
            x_pos (PointUnit):

        Returns: FlowableSection
        """
        for section in self.section_list:
            if section.x_flowable_space_pos <= x_pos <= section.x_flowable_space_pos + section.length:
                return section
        else:
            raise PointOutsideSectionError

    def scene_space_coord_of_flowable_space_coord(self, x_pos, y_pos):
        """
        Find the position in scene space of a given position in flowable space
            (the position in the virtual single-long-rectangle)

        Args:
            x_pos (PointUnit): In flowable space
            y_pos (PointUnit): In flowable space

        Returns: (PointUnit, PointUnit) representing (x_pos, y_pos) in scene space
        """
        containing_section = self.section_at_flowable_space_coord(x_pos)
        scene_space_pos_x = containing_section.x_scene_space_pos + (x_pos - containing_section.x_flowable_space_pos)
        # WARNING: This y calculation assumes that y_pos is relative to the top of flowable space.
        # Might cause confusion when mixing coordinate systems in real objects
        scene_space_pos_y = containing_section.y_scene_space_pos + y_pos
        return scene_space_pos_x, scene_space_pos_y


    def auto_build_sections(self):
        """
        Populate ``self.section_list`` automatically by placing sections leading up to the page margin,
        wrapping around the page and across page breaks.
        
        Returns: None
        """
        
        length_remaining = self.length
        current_flowable_space_pos_x = PointUnit(0)
        current_scene_pos_x = self.starting_scene_pos_x
        current_scene_pos_y = self.starting_scene_pos_y
        current_page = self.starting_page
        # As long as there is room to pass the page margin, add a new section
        while length_remaining > PointUnit(0):
            # Add the section
            distance_to_margin = current_page.right_margin_pos - current_scene_pos_x
            if length_remaining > distance_to_margin:
                section_length = distance_to_margin
            else:
                section_length = distance_to_margin
            self.section_list.append(FlowableSection(self, current_flowable_space_pos_x, section_length,
                                                     current_scene_pos_x, current_scene_pos_y))

            # Move positions to where the next section should go
            # If there isn't room below the new section for another section, make it a page break as well
            is_also_page_break = (current_scene_pos_y + (self.height * PointUnit(2)) + self.default_vertical_padding >
                                  current_page.bottom_margin_pos)
            if is_also_page_break:
                current_page = self.document.get_next_page_or_extend_last(current_page)
                current_scene_pos_y = current_page.top_margin_pos
                self.section_list[-1].terminating_line_break.is_also_page_break = True  # Messy?
            else:
                current_scene_pos_y += self.height + self.default_vertical_padding
            current_scene_pos_x = current_page.left_margin_pos
            current_flowable_space_pos_x += section_length
            length_remaining -= section_length


