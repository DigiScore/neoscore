from typing import Optional

from neoscore.core.break_opportunity import BreakOpportunity
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject


class BreakHint(PositionedObject, BreakOpportunity):

    """A standalone invisible break opportunity.

    When placed in a :obj:`.Flowable`, this signals to the flowable that a break can be
    performed here.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
    ):
        """
        Args:
            pos: The position of the object relative to its parent
            parent: The parent object.
        """
        PositionedObject.__init__(self, pos, parent)
        BreakOpportunity.__init__(self)
