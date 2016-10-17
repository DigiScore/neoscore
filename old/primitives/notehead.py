# from PySide.QtGui import QGraphicsItem, QFont
import brown.music_string_glyph
# from PySide.QtCore import QRectF
from brown.graphic_object import GraphicObject
from brown.named_pitch import NamedPitch
# from brown.note_column import NoteColumn
from brown.tools import pitch_tools
from .music_font import MusicFont
from .staff_unit import StaffUnit
from .staff_object import StaffObject


class Notehead(StaffObject):
    """
    Data container for Noteheads.

    Does not actually contain any QGraphicsItem objects. Any drawn notehead must be contained within a NoteColumn
    """
    def __init__(self, named_pitch, style, parent_column):
        """
        Args:
            named_pitch (NamedPitch or tuple): NamedPitch or tuple representation of its init args
                (pitch_number, letter, accidental, octave)
            style (str): The style of the notehead. Supported styles include: ``open triangle``, ``open diamond``,
            ``solid diamond``, ``open whole triangle``, ``open normal``, ``open whole normal``,
            ``open whole diamond``, ``solid triangle``, ``solid normal``
            parent_column (NoteColumn): parent_column must refer to an existing NoteColumn in order to draw.
                [NOT TRUE ANYMORE]If a Notehead is initialized within a NoteColumn.__init__(), the parent_column will automatically be
                assigned, so the default None may be used
        """
        #   NoteColumn contain a list of all its children Graphic Objects?
        self.parent_column = parent_column
        self.named_pitch = named_pitch
        self.style = style
        StaffObject.__init__(self, self.parent_column.parent_staff, self.parent_column.x_staff_unit_pos,
                             self.staff_position)

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
    def named_pitch(self):
        """NamedPitch: """
        return self._named_pitch

    @named_pitch.setter
    def named_pitch(self, new_named_pitch):
        if isinstance(new_named_pitch, NamedPitch):
            self._named_pitch = new_named_pitch
        elif isinstance(new_named_pitch, tuple) and len(new_named_pitch) <= 4:
            self.named_pitch = NamedPitch(*new_named_pitch)
        else:
            raise TypeError('Notehead.named_pitch must be a NamedPitch object or a tuple representing one'
                            'in the form of its kwargs')

    @property
    def staff_position(self):
        """
        StaffUnit: The position where this Notehead should appear in ``self.parent_staff``

        Returns: StaffUnit where a value of ``0`` represents the center staff line.
        """
        # Find the pitch_position of the clef nearest to the left
        clef_pitch_position = self.parent_column.parent_staff.clef_at_position(
                self.parent_column.x_staff_unit_pos).pitch_position
        # Return the distance between a dummy NamedPitch representing the center line of the staff and self.named_pitch
        # TODO: is there a more efficient way to do this than constructing a dummy NamedPitch?
        #   Maybe just use a tailor-made version of find_letter_distance?
        return StaffUnit(pitch_tools.find_letter_distance(
                NamedPitch(pitch_number=clef_pitch_position, accidental='natural'), self.named_pitch))

    @property
    def ledgers_needed(self):
        """
        Calculates the number of ledger lines needed for this Notehead

        Returns: (int, int) representing (number of ledgers, direction) where direction == 1 means up and -1 means down
        """
        # Find whether the staff_position is above or below 0
        if self.staff_position > 0:
            direction = 1
        else:
            direction = -1
        line_count = self.staff_attributes.line_count
        truncuated_staff_positition = abs(self.staff_position.value) - (line_count - 1)
        # If no ledgers are needed, return
        if truncuated_staff_positition < 2:
            return 0, direction
        return divmod(truncuated_staff_positition, 2)[0], direction

    @property
    def needs_ledgers(self):
        """
        Whether or not the notehead will require ledger lines to draw

        Returns: bool
        """
        # Code taken & modified from self.ledgers_needed
        truncuated_staff_positition = abs(self.staff_position) - (self.parent_column.parent_staff.line_count - 1)
        # If no ledgers are needed, return
        if truncuated_staff_positition < 2:
            return False
        else:
            return True


    @property
    def style(self):
        """
        str: The style of the notehead. Supported styles include: ``open triangle``, ``open diamond``, 
            ``solid diamond``, ``open whole triangle``, ``open normal``, ``open whole normal``, 
            ``open whole diamond``, ``solid triangle``, ``solid normal``
        """
        return self._style

    @style.setter
    def style(self, new_style):
        if not isinstance(new_style, str):
            raise TypeError('Notehead.style must be a str')
        self._style = new_style

    @property
    def show_accidental(self):
        """bool: Determines whether the accidental should be drawn by the parent NoteColumn"""
        return self._show_accidental

    @show_accidental.setter
    def show_accidental(self, new_show_accidental):
        if not isinstance(new_show_accidental, bool):
            raise TypeError('Notehead.show_accidental must be a bool')
        self._show_accidental = new_show_accidental

    def build_glyph(self):
        self.glyph = NoteheadGlyph(self)
        return self.glyph


class NoteheadGlyph(brown.music_string_glyph.MusicStringGlyph):

        def __init__(self, notehead):
            """
            Args:
                notehead (Notehead):
            """

            # Determine string from style
            symbol_dict = {'solid normal': '\uE13E', 'open normal': '\uE13F', 'open whole normal': '\uE169',
                           'solid diamond': '\uE1A2', 'open diamond': '\uE1A1', 'open whole diamond': '\uE1A0',
                           'solid triangle': '\uE1A6', 'open triangle': '\uE1A4', 'open whole triangle': '\uE1A3'}
            try:
                glyph_string = symbol_dict[notehead.style]
            except KeyError:
                # TODO: allow error message to enumerate valid values, maybe using symbol_dict.keys() with a ''.join somehow
                raise ValueError('shape_style of "%s" is invalid.' % notehead.style)

            # init
            # This use of scale=staff_size/17.0 assumes 17.0 is the default, may need to be tweaked
            staff_height = notehead.staff_attributes.height
            brown.music_string_glyph.MusicStringGlyph.__init__(self, notehead.parent_staff.glyph, notehead.scene,
                                                               glyph_string,
                                                               notehead.x_pos, notehead.y_pos, MusicFont('Gonville'),
                                                               notehead.staff_attributes,
                                                               scale=staff_height.value / 17.0)
