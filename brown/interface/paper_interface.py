from PyQt5.QtGui import QPageLayout, QPageSize
from PyQt5.QtCore import QSize, QMarginsF

from brown.config import config
from brown.interface.qt_to_util import unit_to_qt_float


class PaperInterface(QPageLayout):

    def __init__(self, paper):
        """Initialize a QPageLayout from a Paper object

        Args:
            paper (Paper):
        """
        # Scaling ratio for Qt point 72dpi -> config.PRINT_DPI
        ratio = 72 / config.PRINT_DPI
        QPageLayout.__init__(
            self,
            QPageSize(
                QSize(
                    unit_to_qt_float(paper.width) * ratio,
                    unit_to_qt_float(paper.height) * ratio,
                ),
            ),
            QPageLayout.Portrait,
            QMarginsF(
                unit_to_qt_float(paper.margin_left) * ratio,
                unit_to_qt_float(paper.margin_top) * ratio,
                unit_to_qt_float(paper.margin_right) * ratio,
                unit_to_qt_float(paper.margin_bottom) * ratio,
            )
        )
