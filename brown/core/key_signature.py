from brown.core.accidental import Accidental
from brown.models.accidental_type import AccidentalType
from brown.core.object_group import ObjectGroup
from brown.core.staff_object import StaffObject
from brown.core.music_text import MusicText
from brown.models.key_signature_type import KeySignatureType
from brown.models.clef_type import ClefType
from brown.utils.point import Point
from brown.utils.units import Unit


class KeySignature(ObjectGroup, StaffObject):

    """A logical and graphical key signature.

    The signature will be rendered initially at the given `pos_x`,
    and at the beginning of subsequent lines until a new
    `KeySignature` is encountered.

    All traditional key signatures (those included in `KeySignatureTypes`)
    are supported by this class. Nontraditional key signatures could
    be implemented in a fairly straightforward way in a subclass of this.
    """

    __sharp_positions = {
        'f': (0, 0),
        'c': (1, 1.5),
        'g': (2, -0.5),
        'd': (3, 1),
        'a': (4, 2.5),
        'e': (5, 0.5),
        'b': (6, 2),
    }
    __flat_positions = {
        'b': (0, 2),
        'e': (1, 0.5),
        'a': (2, 2.5),
        'd': (3, 1),
        'g': (4, 3),
        'c': (5, 1.5),
        'f': (6, 3.5),
    }
    sharp_positions = {
        ClefType.treble: __sharp_positions,
        ClefType.bass: {key: (value[0], value[1] + 1)
                        for key, value in __sharp_positions.items()},
        ClefType.alto: {key: (value[0], value[1] + 0.5)
                        for key, value in __sharp_positions.items()},
        ClefType.tenor: {key: (value[0], value[1] - 0.5)
                         for key, value in __sharp_positions.items()}
    }

    flat_positions = {
        ClefType.treble: __flat_positions,
        ClefType.bass: {key: (value[0], value[1] + 1)
                        for key, value in __flat_positions.items()},
        ClefType.alto: {key: (value[0], value[1] + 0.5)
                        for key, value in __flat_positions.items()},
        ClefType.tenor: {key: (value[0], value[1] - 0.5)
                         for key, value in __flat_positions.items()}
    }

    def __init__(self, pos_x, staff, key_signature_type):
        """
        Args:
            pos_x (Unit): The x position relative to the parent staff.
            staff (Staff): The parent staff
            key_signature_type (KeySignatureType or str): A description of the
                key signature. Any KeySignatureType may be used, or a str
                of one's name.
        """
        ObjectGroup.__init__(self, Point(pos_x, staff.unit(0)),
                             staff)
        StaffObject.__init__(self, staff)
        self._key_signature_type = (
            key_signature_type
            if isinstance(key_signature_type, KeySignatureType)
            else KeySignatureType[key_signature_type])
        self._create_pseudo_accidentals()

    ######## PUBLIC PROPERTIES ########

    @property
    def key_signature_type(self):
        """KeySignatureType: A logical description of the key signature."""
        return self._key_signature_type

    @property
    def length(self):
        """`KeySignature`s extend until another is found in the staff."""
        return self.staff.distance_to_next_of_type(self)

    ######## INNER CLASSES ########

    class _KeySignatureAccidental(MusicText):
        """An visual accidental.

        This should only be used within this class.
        """
        def __init__(self, occurrence_offset, clef_offset, text, parent,
                     font, scale_factor, length):
            super().__init__(Point(Unit(0), Unit(0)), text, parent,
                             font, scale_factor)
            self.clef_offset = clef_offset
            self.mid_system_offset = occurrence_offset
            self.recurring_offset = Point(
                self.mid_system_offset.x + self.clef_offset,
                self.mid_system_offset.y)
            self._length = length

        @property
        def length(self):
            return self._length

        def _render_complete(self, pos):
            self._render_slice(pos + self.mid_system_offset, None)

        def _render_before_break(self, local_start_x, start, stop):
            self._render_slice(start + self.mid_system_offset, None)

        def _render_after_break(self, local_start_x, start, stop):
            self._render_slice(start + self.recurring_offset, None)

        def _render_spanning_continuation(self, local_start_x, start, stop):
            self._render_slice(start + self.recurring_offset, None)

    ######## PRIVATE METHODS ########

    def _create_pseudo_accidentals(self):
        pos_in_staff = self.frame.map_between_items_in_frame(
            self.staff, self).x
        clef = self.staff.active_clef_at(pos_in_staff)
        if clef is None:
            return
        clef_type = clef.clef_type
        # Get extra offset for the clef
        clef_offset = clef._bounding_rect.width + self.staff.unit(0.5)

        for key, value in self.key_signature_type.value.items():
            if value is None:
                continue
            if value == AccidentalType.sharp:
                pos_tuple = KeySignature.sharp_positions[clef_type][key]
            else:
                pos_tuple = KeySignature.flat_positions[clef_type][key]
            pos = Point(self.staff.unit(pos_tuple[0]),
                        self.staff.unit(pos_tuple[1]))
            KeySignature._KeySignatureAccidental(
                pos,
                clef_offset,
                Accidental._canonical_names[value],
                self,
                self.staff.music_font,
                1,
                self.length)
