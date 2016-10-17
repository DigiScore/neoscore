
from .music_string_glyph import MusicStringGlyph
from .shared import brown_config
from .music_font import MusicFont
from .staff_object import StaffObject

class Rest(StaffObject):
    """
    Data container for Rests
    """
    def __init__(self, parent_column, style, y_staff_unit_pos=0):
        self.parent_column = parent_column
        self.style = style
        StaffObject.__init__(self, self.parent_column.parent_staff, self.parent_column.x_staff_unit_pos,
                             y_staff_unit_pos)

    @property
    def parent_column(self):
        """NoteColumn: the NoteColumn to which this Notehead belongs"""
        return self._parent_column

    @parent_column.setter
    def parent_column(self, new_parent_column):
        # if not isinstance(new_parent_column, NoteColumn):
        #     raise TypeError('Notehead.parent_column must be a NoteColumn object')
        self._parent_column = new_parent_column


    @property
    def style(self):
        """
        str: The style of the notehead. Supported styles include: '2', '1', '1/2', '1/4', '1/8', '1/16', 
            '1/32', '1/64', '1/128', '1/256', '1/512' 
        """
        return self._style

    @style.setter
    def style(self, new_style):
        if not isinstance(new_style, str):
            raise TypeError('Notehead.style must be a str')
        self._style = new_style

    def build_glyph(self):
        self.glyph = RestGlyph(self)
        return self.glyph


class RestGlyph(MusicStringGlyph):
    #
    # def __init__(self, parent, scene, x_pos, y_pos, staff, style='1/4'):
    #     """
    #
    #     Args:
    #         parent:
    #         scene:
    #         x_pos:
    #         y_pos:
    #         staff (Staff):
    #         style (str):
    #
    #
    #     Returns:
    #
    #     """
    #
    #
    #
    #     # Determine string from style
    #     # TODO: What about note values smaller than 64th's?
    #     symbol_dict = {'2': '\uE15C', '1': '\uE163', '1/2': '\uE167', '1/4': '\uE15D', '1/8': '\uE15E', '1/16': '\uE156',
    #                    '1/32': '\uE160', '1/64': '\uE161'}
    #
    #     try:
    #         glyph_string = symbol_dict[style]
    #     except KeyError:
    #         # TODO: allow error message to enumerate valid values, maybe using symbol_dict.keys() with a ''.join somehow
    #         raise ValueError('shape_style of "%s" is invalid.' % style)
    #
    #     # init
    #     # This use of scale=staff_size/17.0 assumes 17.0 is the default, may need to be tweaked
    #     MusicStringGlyph.__init__(self, parent, scene, glyph_string,
    #                               x_pos, y_pos, MusicFont('Gonville'), staff, scale=staff.staff_height / 17.0)


    def __init__(self, rest):
        """
        Args:
            rest (Rest):
        """

        # Determine string from style
        # TODO: What about note values smaller than 64th's?
        symbol_dict = {'2': '\uE15C', '1': '\uE163', '1/2': '\uE167', '1/4': '\uE15D', '1/8': '\uE15E', '1/16': '\uE156',
                       '1/32': '\uE160', '1/64': '\uE161'}

        try:
            glyph_string = symbol_dict[rest.style]
        except KeyError:
            # TODO: allow error message to enumerate valid values, maybe using symbol_dict.keys() with a ''.join somehow
            raise ValueError('shape_style of "%s" is invalid.' % rest.style)

        # init
        # This use of scale=staff_size/17.0 assumes 17.0 is the default, may need to be tweaked
        MusicStringGlyph.__init__(self, rest.parent, rest.scene, glyph_string,
                                  rest.x_pos, rest.y_pos, MusicFont('Gonville'), rest.staff_attributes,
                                  scale=rest.parent_staff.staff_height.value / 17.0)