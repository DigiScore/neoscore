#!/usr/bin/env python
from .staff import Staff
from PySide.QtGui import QGraphicsItemGroup
from .named_pitch import NamedPitch
from .shared import brown_config
from .staff_object import StaffObject
from .notehead import Notehead
from .stem import Stem
from .accidental import AccidentalObject
from .ledger_line import LedgerLine
from .staff_unit import StaffUnit
from .rest import Rest
from .rhythm_dot import RhythmDot
from .tools.staff_tools import y_of_staff_pos, line_or_space, needs_ledgers
from .rhythmic_value import RhythmicValue
from .time_value import TimeDuration
from .tools.unit_tools import staff_unit_to_pt
from .tools.pitch_tools import find_active_accidental_in_staff
from .tools.rhythm_tools import rhythm_can_have_flag
from .flag import Flag
from .rectangle import Rectangle
from .staff_unit_rectangle import StaffUnitRectangle


class NoteColumn(StaffObject):
    """
    A staff-bound object containing at least one ``Notehead`` object.
    """

    def __init__(self, parent_staff, x_staff_unit_pos, contents,
                 duration=None, has_stem=True, beam_flag=None):
        """
        Args:
            parent_staff (Staff):
            x_staff_unit_pos (StaffUnit or float or int): Horizontal position
                relative to
                the parent_staff in StaffUnit units
            contents (list[Notehead or Rest]): Note that the parent_column of
                all content objects will be automatically assigned
                to this NoteColumn.
        """
        StaffObject.__init__(self, parent_staff, x_staff_unit_pos, 0)
        self.has_stem = has_stem
        self.stem_flipped = False
        self.duration = duration
        self.beam_flag = beam_flag
        # Make sure notes is a list, place in one if not
        self.supporting_contents = []
        if not isinstance(contents, list):
            contents = [contents]
        # Populate notes
        self.contents = []
        for item in contents:
            if isinstance(item, Notehead) or isinstance(item, Rest):
                if item.parent_column != self:
                    item.parent_column = self
                self.contents.append(item)
            else:
                raise TypeError('All notes in NoteColumn.__init__() '
                                'must be of type Notehead or Rest')

        # Initialize all glyphs
        # self.build_glyph()
        
    def add_spanner(style, end):
        """
        Add a spanner of ``style`` ending at ``end``.
        
        If ``end`` is a ``NoteColumn``, terminate at that column.
        If ``end`` is an ``int``, terminate ``end`` columns forward
        in the parent staff. If ``end`` is a unit
        (``mm``, ``inch``, ``StaffUnit``, etc.), or a tuple of units (x, y),
        end graphically at that point
        """
        # TODO: Build me
        # TODO: Build convenience functions for indiviual spanner
        #styles which just call this
        # Questions:
        # 	  - How can the parent context be looked up elegantly without assuming what
        #		the parent context is? Not all columns exist in staves, but that doesn't
        #		mean that they don't contain ordered columns. Maybe some kind of ordered
        #		column container class that applicable classes inherit from? 
        #		Multiple inheritance, ew...
        pass
      
        
    @property
    def contents(self):
        """
        list[StaffObject]:
        """
        # TODO: How should contents really be handled when considering that
        # ledger lines and accidentals are now StaffObjects too
        return self._notes

    @contents.setter
    def contents(self, new_notes):
        # Make sure that notes is a list of Notehead instances
        if isinstance(new_notes, list):
            # Verify that the items in new_notes are all Notehead objects
            #   [Is this necessary? Could be slow if this is called often]
            for item in new_notes:
                if not (isinstance(item, Notehead) or isinstance(item, Rest)):
                    raise TypeError('NoteColumn.notes must be a list of Notehead or Rest instances')
            self._notes = new_notes
        else:
            # Wrap in a list
            if not isinstance(new_notes, Notehead):
                raise TypeError('NoteColumn.notes must be a list of Notehead  or Rest instances')
            self._notes = [new_notes]

    @property
    def supporting_contents(self):
        """list: list of contents in the NoteColumn which are not Notehead or Rest objects.
        These objects include AccidentalObject, RhythmDot, LedgerLine, Stem"""
        return self._supporting_contents

    @supporting_contents.setter
    def supporting_contents(self, new_supporting_contents):
        if not isinstance(new_supporting_contents, list):
            new_supporting_contents = [new_supporting_contents]
        self._supporting_contents = new_supporting_contents

    @property
    def duration(self):
        """RhythmicValue, TimeDuration, or None: The duration value of the NoteColumn.

        The value may be set either as a RhythmicValue, tuple representation of a RhythmicValue,
        TimeDuration, float or int representation of a TimeDuration, or None."""
        return self._duration

    @duration.setter
    def duration(self, new_duration):
        # Try to convert to valid types if possible
        if isinstance(new_duration, tuple) and len(new_duration) <= 2:
            # A tuple of len 2 becomes a RhythmicValue
            new_duration = RhythmicValue(*new_duration)
        elif isinstance(new_duration, str):
            # A str becomes a RhythmicValue
            new_duration = RhythmicValue(new_duration)
        elif isinstance(new_duration, float) or isinstance(new_duration, int):
            # A float or int becomes a TimeDuration
            new_duration = TimeDuration(new_duration)
        elif ((not isinstance(new_duration, RhythmicValue)) and
                  (not isinstance(new_duration, TimeDuration)) and
                  (new_duration is not None)):
            # Otherwise, if this isn't one of the valid types, it can't be converted to one. Raise TypeError.
            raise TypeError('NoteColumn.duration must be set to either '
                            'RhythmicValue, tuple, TimeDuration, float, int, or None')
        self._duration = new_duration

    @property
    def column_height(self):
        """StaffUnit: The total height of this note_column in staff units measured from its lowest item in
        self.contents to its highest. If this NoteColumn contains one or no items, the value is 0."""
        # If self.contents contains 1 or fewer items, return 0 by default
        # Possibly later on this behavior could be changed to account for potentially taller items
        if len(self.contents) <= 1:
            return StaffUnit(0)
        # (This assumes that everything in self.contents has the attribute staff_position -
        #  could easily lead to bugs if the scope of self.contents is expanded)
        staff_pos_list = [item.staff_position for item in self.contents]
        return StaffUnit(max(staff_pos_list) - min(staff_pos_list))

    @property
    def beam_flag(self):
        """str: Flag indicating how beaming should be handled at this NoteColumn.
        Legal values are: ``'NO_BEAM'``, ``'BEAM_RIGHT'``, ``'BEAM_LEFT'``, ``'BEAM_THROUGH'``, and ``None``.
        Setting to ``None`` will default to ``'NO_BEAM'``"""
        return self._beam_state

    @beam_flag.setter
    def beam_flag(self, new_beam_state):
        if new_beam_state is None:
            new_beam_state = 'NO_BEAM'
        elif new_beam_state not in ['NO_BEAM', 'BEAM_RIGHT', 'BEAM_LEFT', 'BEAM_THROUGH']:
            raise ValueError("BeamState.state of %s is invalid. Legal values are: "
                             "['NO_BEAM', 'BEAM_RIGHT', 'BEAM_LEFT', 'BEAM_THROUGH']" % new_beam_state)
        self._beam_state = new_beam_state

    @property
    def outermost_item(self):
        """(Notehead or Rest): The item in self.contents furthest from the staff center"""
        return max(self.contents, key=lambda item: abs(item.staff_position.value))

    @property
    def stem_flipped(self):
        """bool: Determines whether or not the default stem_direction should be flipped."""
        return self._stem_flipped

    @stem_flipped.setter
    def stem_flipped(self, new_value):
        if not isinstance(new_value, bool):
            raise TypeError
        self._stem_flipped = new_value

    @property
    def stem_direction(self):
        """int: -1 or 1. Indicates the direction the stem should face, taking into account ``self.stem_flipped``"""
        if self.outermost_item.staff_position < 0:
            direction = 1
        else:
            direction = -1
        if self.stem_flipped:
            direction *= -1
        return direction

    @property
    def noteheads_split(self):
        """bool: True if the Notehead objects contained in self.content will need to be split across the stem
        to avoid collisions"""
        # if len(self.contents) is 1 or less (0), then the notehead couldn't be split across the stem
        if not (len(self.contents) <= 1):
            for item_index in range(len(self.contents)):
                if abs(self.contents[item_index].staff_position.value -
                               self.contents[item_index - 1].staff_position.value) <= 1:
                    return True
        # If we've made it this far then the Notehead objects do not collide, return False
        return False

    @property
    def notes_bounding_box(self):
        """StaffUnitRectangle: A rectangle approximately surrounding all noteheads and rests in ``self.contents``.
        Coordinates are in 72-dpi units relative to self.parent_staff.glyph"""
        rect_x = self.x_staff_unit_pos
        # rect_y = y_of_staff_pos(self.parent_staff, max(self.contents, key=lambda item: item.staff_position).staff_position, 1)
        # Previous approach ^ added 1 to rect_y, should this be done here too?
        rect_y = max(self.contents, key=lambda item: item.staff_position.value).staff_position
        # Determine if the column is split (meaning noteheads are spread across both sides of the stem)
        # and set rect_width accordingly

        # notehead_width = self.parent_staff.approx_notehead_width
        notehead_width = self.staff_attributes.approx_notehead_width
        rect_width = notehead_width
        if self.noteheads_split:
            rect_width = rect_width.value * 2
        # Adjust rect_width slightly to the right
        rect_width += notehead_width * brown_config.default_notehead_padding
        # Convert rect_height to 72-dpi units
        rect_height = self.column_height

        return StaffUnitRectangle(rect_x, rect_y, rect_width, rect_height)

    def find_ledgers_needed(self):
        """
        Iterates through self.notes and finds the number of ledgers needed both above and below the staff.
        
        It is important to find (and draw) the number of needed ledgers within NoteColumn to avoid
        creating duplicated ledger lines
        
        Returns: (int, int) representing (number below, number above)
        """
        ledgers_below = 0
        ledgers_above = 0
        for note in self.contents:
            note_ledgers = note.ledgers_needed
            # continue if no ledgers are needed
            if note_ledgers[0] == 0:
                continue

            if note_ledgers[1] == -1:
                # If these ledger lines are below the staff
                if note_ledgers[0] > ledgers_below:
                    ledgers_below = note_ledgers[0]
            else:
                # If these ledger lines are above the staff
                if note_ledgers[0] > ledgers_above:
                    ledgers_above = note_ledgers[0]
        return ledgers_below, ledgers_above

    @property
    def in_slur(self):
        """
        Whether or not this NoteColumn is contained in a slur
        """
        # Check with staff (or whatever parent structure is) to see if a slur passes over this
        # TODO: Build me
        pass
    
    @property
    def in_dynamic_spanner(self):
        """
        Whether or not this NoteColumn is contained in a dynamic related spanner
        """
        # Check with staff (or whatever parent structure is) to see if a dynamic related spanner
        # passes over this
        # TODO: Build me
        pass
      
    # ------------------------------------------------------------------------------------------------------------------
    def build_glyph(self):
        # In NoteColumn objects, self.glyph refers to a list of glyphs
        # including noteheads, ledger lines, accidentals, rest glyphs, stem lines, and others
        # Initialize self.glyph as an empty list
        self.glyph = []
        #############################################################
        # STEP ONE: Add supporting objects to self.contents
        #############################################################
        # TODO: build an algorithm to pack accidentals neatly
        # Build ledger line glyphs -------------------------------------------------------------------------------------
        ledgers_needed = self.find_ledgers_needed()
        for i in range(ledgers_needed[0]):
            # Build ledgers below
            self.supporting_contents.append(LedgerLine(self, (i * -2) - 6))
        for i in range(ledgers_needed[1]):
            # Build ledgers above
            self.supporting_contents.append(LedgerLine(self, (i * 2) + 6))

        # Draw the stem and flag if called for -------------------------------------------------------------------------
        if self.has_stem:
            # Calculate the staff_position_anchor by finding the outermost note in the column
            staff_position_anchor = self.outermost_item.staff_position
            # Find the needed stem_length
            stem_length = StaffUnit((self.column_height.value / 2.0) +
                                    brown_config.default_stem_length.value)
            new_stem = Stem(self, staff_position_anchor, stem_length, self.stem_direction)
            self.supporting_contents.append(new_stem)

            # If self.duration is a RhythmicValue which can have a flag, draw the flag
            if isinstance(self.duration, RhythmicValue) and rhythm_can_have_flag(self.duration):
                # Extend the stem if a tall flag glyph will be required (ie. 32nd note flags)
                if self.duration.base_value > 16:
                    # Add one staff space per flag-let
                    # (Somewhat hacky right now, could possibly be done better by counting powers of 2 or something)
                    new_stem.length += StaffUnit([32, 64, 128, 256, 512, 1024].index(self.duration.base_value) + 1)
                # Calculate flag x position. Shift right slightly
                # flag_x_pos = new_stem.x_pos + (self.parent_staff.approx_notehead_width.value * 0.05)
                self.supporting_contents.append(Flag(self, new_stem.y_staff_unit_stop_pos))

        # Build rest, notehead, and accidental glyphs ------------------------------------------------------------------
        # Re-order self.contents by staff_position in descending order
        self.contents = sorted(self.contents, key=lambda item: item.staff_position, reverse=True)
        # leftmost_notehead_pos = self.x_pos
        last_notehead_flipped = False
        for item_index in range(len(self.contents)):
            current_item = self.contents[item_index]
            previous_item = self.contents[item_index - 1]
            if isinstance(current_item, Notehead) or isinstance(current_item, Rest):
                if isinstance(current_item, Notehead):
                    # Determine whether or not this Notehead should be flipped across the stem
                    # notehead_adjusted_x_pos = self.x_pos
                    if not last_notehead_flipped:
                        # If the last notehead wasn't flipped, check to make sure this one doesn't need to be
                        if previous_item.staff_position == current_item.staff_position + 1:
                            # If the immediately above notehead is 1 staff unit above, flip this notehead
                            last_notehead_flipped = True
                            # notehead_adjusted_x_pos += self.parent_staff.approx_notehead_width * self.stem_direction
                            notehead_width = self.staff_attributes.approx_notehead_width
                            current_item.x_staff_unit_pos += StaffUnit(notehead_width.value * self.stem_direction)
                            current_item.x_pos = current_item.x_staff_unit_pos.in_points(self.staff_attributes)
                            # leftmost_notehead_pos = min(notehead_adjusted_x_pos, self.x_pos)
                    # self.glyph.append(NoteheadGlyph(self.parent.glyph, self.parent_staff.scene,
                    #                                 notehead_adjusted_x_pos, y_pos,
                    #                                 self.parent_staff,
                    #                                 current_item.style))
                    # self.glyph.append(current_item.build_glyph())
                    # Determine whether an accidental is needed or not
                    active_accidental = find_active_accidental_in_staff(self.parent_staff, self.x_pos,
                                                                        current_item.named_pitch.letter,
                                                                        current_item.named_pitch.octave)
                    if active_accidental != current_item.named_pitch.accidental:
                        # Add an accidental to self.contents
                        # Move the accidental two staff units left
                        # accidental_position = leftmost_notehead_pos - (self.parent_staff.staff_unit_dist * 2)
                        accidental_x_offset = StaffUnit(-2)
                        if self.noteheads_split:
                            accidental_x_offset += StaffUnit(-2.5)
                        self.supporting_contents.append(AccidentalObject(current_item, accidental_x_offset))

                elif isinstance(current_item, Rest):
                    # self.glyph.append(RestGlyph(self.parent.glyph, self.parent_staff.scene,
                    #                             self.x_pos, y_pos, self.parent_staff,
                    #                             current_item.style))
                    pass

                # Draw rhythm dots if needed
                if isinstance(self.duration, RhythmicValue) and self.duration.dot_count:
                    # If the dots would land on a staff line, shift up one staff unit
                    dot_group_y_staff_pos = current_item.staff_position
                    if (line_or_space(dot_group_y_staff_pos) == 'line' and not
                            needs_ledgers(self.staff_attributes, dot_group_y_staff_pos)):
                        dot_group_y_staff_pos += 1
                    for i in range(self.duration.dot_count):
                        self.supporting_contents.append(RhythmDot(current_item, i + 3))

        #############################################################
        # STEP TWO: Build all glyphs
        #############################################################
        for item in self.contents:
            self.glyph.append(item.build_glyph())
        for item in self.supporting_contents:
            self.glyph.append(item.build_glyph())
