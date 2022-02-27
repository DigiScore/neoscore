from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from brown.interface.paper_interface import PaperInterface
from brown.utils.units import Inch, Mm, Unit


@dataclass(frozen=True)
class Paper:

    """A specification for a paper geometry used to lay out pages"""

    width: Unit
    height: Unit
    margin_top: Unit
    margin_right: Unit
    margin_bottom: Unit
    margin_left: Unit
    gutter: Unit
    live_width: Unit = field(init=False)
    live_height: Unit = field(init=False)

    def __post_init__(self):
        # This hack is needed to assign derived fields on frozen dataclasses
        # See https://stackoverflow.com/a/54119384/5615927
        super().__setattr__(
            "live_width",
            self.width - self.gutter - self.margin_left - self.margin_right,
        )
        super().__setattr__(
            "live_height", self.height - self.margin_bottom - self.margin_top
        )

    ######## PUBLIC METHODS ########

    def make_rotation(self):
        """Create a 90 degree clockwise rotation of this `Paper`.

        The `gutter` field is not changed in this new `Paper`.

        Returns: Paper
        """
        return Paper(
            self.height,
            self.width,
            self.margin_left,
            self.margin_top,
            self.margin_right,
            self.margin_bottom,
            self.gutter,
        )

    ######## PRIVATE METHODS ########

    def _to_interface(self):
        """Construct and return a PaperInterface based on this Paper.

        Returns: PaperInterface
        """
        return PaperInterface(self)


# Common Paper template instances are provided
class PaperTemplate(Enum):
    A4 = Paper(Mm(210), Mm(297), Mm(20), Mm(20), Mm(20), Mm(20), Mm(0))
    Letter = Paper(Inch(8.5), Inch(11), Inch(1), Inch(1), Inch(1), Inch(1), Inch(0.3))
