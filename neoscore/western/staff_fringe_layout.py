from dataclasses import dataclass, field

from neoscore.core.units import ZERO, Unit


@dataclass(frozen=True)
class StaffFringeLayout:

    """Layout specification for a :obj:`.Staff` fringe.

    Each field except ``pos_x_in_staff`` describes an X-axis position relative to the
    start of the staff's live area. In flowables, that start point is typically the
    beginning of the flowable :obj:`.NewLine`. Outside flowables, that start point is
    the X-axis position of the staff.

    Since fringes extend to the left of this reference point, the values here will
    typically be negative.
    """

    pos_x_in_staff: Unit
    """The staff position of the line where this fringe is placed.

    In staves outside flowables, this will always be ``ZERO``.
    """

    staff: Unit
    """The starting position of the drawn staff in the fringe."""

    clef: Unit
    """The clef's position"""

    key_signature: Unit
    """The key signature's position, if any.

    If there is no key signature this will be ``ZERO``.
    """

    time_signature: Unit = field(default_factory=lambda: ZERO)
    """The time signature's position, if any.

    If there is no time signature this will be ``ZERO``.
    """
