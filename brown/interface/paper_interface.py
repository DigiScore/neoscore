from PyQt5.QtCore import QMarginsF, QSize
from PyQt5.QtGui import QPageLayout, QPageSize

from brown import constants

# TODO MEDIUM Refactor to use the main interface pattern by making
# this have the ability to create a qt QPageLayout object, but not
# itself be one.


class PaperInterface(QPageLayout):

    """A thin conversion layer between `Paper` and `QPageLayout`."""

    def __init__(self, paper):
        """Initialize a QPageLayout from a Paper object

        Margins are in the given `paper` are ignored so that,
        when used for printing, this interface allows printing
        over the page margins.

        Args:
            paper (Paper):
        """
        # Scaling ratio for Qt point 72dpi -> constants.PRINT_DPI
        ratio = 72 / constants.PRINT_DPI
        QPageLayout.__init__(
            self,
            QPageSize(
                QSize(
                    paper.width.base_value * ratio,
                    paper.height.base_value * ratio,
                ),
            ),
            QPageLayout.Portrait,
            # Margins are implemented at a higher level
            QMarginsF(0, 0, 0, 0),
        )
