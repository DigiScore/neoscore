from dataclasses import dataclass, field

from PyQt5.QtCore import QMarginsF, QSize
from PyQt5.QtGui import QPageLayout, QPageSize

from neoscore import constants
from neoscore.utils.units import Unit


@dataclass(frozen=True)
class PaperInterface:

    width: Unit
    height: Unit
    qt_object: QPageLayout = field(init=False)

    def __post_init__(self):
        # Scaling ratio for Qt point 72dpi -> constants.PRINT_DPI
        ratio = 72 / constants.PRINT_DPI
        super().__setattr__(
            "qt_object",
            QPageLayout(
                QPageSize(
                    QSize(
                        int(self.width.base_value * ratio),
                        int(self.height.base_value * ratio),
                    ),
                ),
                QPageLayout.Portrait,
                # Margins are implemented at a higher level
                QMarginsF(0, 0, 0, 0),
            ),
        )
