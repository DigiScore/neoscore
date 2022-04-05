from neoscore.core.units import Unit
from neoscore.western.clef import Clef
from neoscore.western.clef_type import ClefTypeDef
from neoscore.western.staff import Staff


class InvisibleClef(Clef):

    """A non-printing clef.

    This is useful in contexts where staves are used with implied clefs.
    """

    def __init__(self, pos_x: Unit, staff: Staff, clef_type: ClefTypeDef):
        # Hackily create a superclass Clef, then just overwrite its text
        # this is slightly inefficient but probably fine
        super().__init__(pos_x, staff, clef_type)
        self.text = ""
