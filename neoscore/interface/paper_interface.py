from dataclasses import dataclass, field

from PyQt5.QtCore import QMarginsF, QSize
from PyQt5.QtGui import QPageLayout, QPageSize

from neoscore.core.units import Unit


# TODO HIGH  I think now that we're off Qt's printing functionality we can delete this
@dataclass(frozen=True)
class PaperInterface:

    width: Unit
    height: Unit
    qt_object: QPageLayout = field(init=False)

    def __post_init__(self):
        super().__setattr__(
            "qt_object",
            QPageLayout(
                QPageSize(
                    QSize(
                        int(self.width.base_value),
                        int(self.height.base_value),
                    ),
                ),
                QPageLayout.Portrait,
                # Margins are implemented at a higher level
                QMarginsF(0, 0, 0, 0),
            ),
        )
