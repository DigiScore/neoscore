from brown.models.beat import Beat
from brown.utils.units import Unit


class BeatSizeController:

    """A controller setting the default concrete beat unit following it.

    This is for use in the context of a Staff where these controllers are
    used to manipulate layout by changing the type of Beat used.

    For instance is a measure is filled with two half notes, the graphical
    distance between these objects can be controlled simply by inserting
    BeatSizeControllers changing the ratio of a half note (Beat(1, 2)) to
    a Unit.

    Public Attributes:
        x (Beat): Where this controller goes into effect. This should
            be an *abstract* beat (without a defined Beat/Unit ratio).
        beat (ConcreteBeat): The type of Concrete beat in effect following
            this controller
    """

    def __init__(self,
                 pos_x,
                 whole_note_size,
                 constant_offset,
                 name=None):
        """
        Args:
            pos_x (Beat):
            whole_note_size (Unit): The length of a Beat(1, 1)
            constant_offset (Unit): A constant offset for all conversions.
            name (str): The name for the concrete Beat class.
                If not specified, 'ConcreteBeat' is used.
        """
        self.x = pos_x
        self.beat = Beat.make_concrete_beat(whole_note_size,
                                            constant_offset,
                                            name)
