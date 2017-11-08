from brown.core.accidental import Accidental
from brown.core.music_text import MusicText
from brown.core.object_group import ObjectGroup
from brown.core.staff_object import StaffObject
from brown.models.accidental_type import AccidentalType
from brown.models.clef_type import ClefType
from brown.models.key_signature_type import KeySignatureType
from brown.utils.point import Point


class KeySignature(ObjectGroup, StaffObject):

    """A logical and graphical key signature.

    The signature will be rendered initially at the given `pos_x`,
    and at the beginning of subsequent lines until a new
    `KeySignature` is encountered.

    All traditional key signatures (those included in `KeySignatureTypes`)
    are supported by this class. Nontraditional key signatures could
    be implemented in a fairly straightforward way in a subclass of this.
    """

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

    ######## PRIVATE METHODS ########

    def _create_pseudo_accidentals(self):
        for key, value in self.key_signature_type.value.items():
            if value is not None:
                _KeySignatureAccidental(
                    self.pos,
                    key,
                    value,
                    self,
                    self.staff.music_font,
                    1,
                    self.length)


class _KeySignatureAccidental(MusicText, StaffObject):
    """A visual accidental.

    This should only be used within `KeySignature`s.
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
    positions = {
        AccidentalType.flat: {
            ClefType.treble: __flat_positions,
            ClefType.bass: {key: (value[0], value[1] + 1)
                            for key, value in __flat_positions.items()},
            ClefType.alto: {key: (value[0], value[1] + 0.5)
                            for key, value in __flat_positions.items()},
            ClefType.tenor: {key: (value[0], value[1] - 0.5)
                             for key, value in __flat_positions.items()}
        },
        AccidentalType.sharp: {
            ClefType.treble: __sharp_positions,
            ClefType.bass: {key: (value[0], value[1] + 1)
                            for key, value in __sharp_positions.items()},
            ClefType.alto: {key: (value[0], value[1] + 0.5)
                            for key, value in __sharp_positions.items()},
            ClefType.tenor: {key: (value[0], value[1] - 0.5)
                             for key, value in __sharp_positions.items()}
        }
    }

    def __init__(self, pos, pitch_letter, accidental_type, key_signature,
                 music_font, scale_factor, length):
        MusicText.__init__(self, pos, Accidental._canonical_names[accidental_type],
                           key_signature, music_font, scale_factor)
        StaffObject.__init__(self, key_signature)
        self._length = length
        self.pitch_letter = pitch_letter
        self.accidental_type = accidental_type

    @property
    def length(self):
        return self._length

    def _overlaps_with_clef(self, clef, padded_clef_width):
        return (self.flowable.map_between_locally(clef, self).x
                < padded_clef_width)

    def _render_occurrence(self, pos, local_start_x):
        """Render one appearance of one key signature accidental.

        Because this performs a lot of nontrivial computation for each
        occurrence of each accidental, this is very inefficient.

        If this proves to be a performance bottleneck in the future,
        there's lots of room for optimization here.
        """

        staff_pos_in_flowable = self.flowable.pos_in_flowable_of(self.staff)
        pos_x_in_staff = local_start_x - staff_pos_in_flowable.x
        clef = self.staff.active_clef_at(pos_x_in_staff)
        if clef is None:
            return
        clef_type = clef.clef_type
        padded_clef_width = clef.bounding_rect.width + self.staff.unit(0.5)
        pos_tuple = _KeySignatureAccidental.positions[
            self.accidental_type][clef_type][self.pitch_letter]
        visual_pos = Point(self.staff.unit(pos_tuple[0]),
                           self.staff.unit(pos_tuple[1])) + pos
        if self._overlaps_with_clef(clef, padded_clef_width):
            visual_pos.x += padded_clef_width
        self._render_slice(visual_pos, None)

    def _render_complete(self, pos, dist_to_line_start=None, local_start_x=None):
        self._render_occurrence(pos, local_start_x)

    def _render_before_break(self, local_start_x, start, stop, dist_to_line_start):
        self._render_occurrence(start, local_start_x)

    def _render_after_break(self, local_start_x, start, stop):
        self._render_occurrence(start, local_start_x)

    def _render_spanning_continuation(self, local_start_x, start, stop):
        self._render_occurrence(start, local_start_x)
