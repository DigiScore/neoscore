from dataclasses import dataclass

from neoscore.core.units import ZERO, Unit


@dataclass(frozen=True)
class StaffFringeLayout:
    pos_x_in_staff: Unit
    staff: Unit
    clef: Unit
    key_signature: Unit
    time_signature: Unit = ZERO
