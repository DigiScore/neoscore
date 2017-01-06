from brown.core.path import Path
from brown.primitives.staff_object import StaffObject


class LedgerLine(Path, StaffObject):

    def __init__(self, pos, parent, length=None):
        """
        Args:
            pos (Point(StaffUnit)):
            parent (StaffObject or Staff):
            length (StaffUnit): Length of the ledger line
        """
        Path.__init__(self, pos, parent=parent)
        StaffObject.__init__(self, parent=parent)
        self._length = length if length is not None else self.staff.unit(0.75)
        self.line_to(self.length, self.staff.unit(0))

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self):
        """int: The length in staff units of the ledger line"""
        return self._length
