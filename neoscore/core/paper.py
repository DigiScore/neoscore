from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from neoscore.core.units import ZERO, Inch, Mm, Unit


@dataclass(frozen=True)
class Paper:

    """A specification for a paper geometry used to lay out pages"""

    width: Unit
    height: Unit
    margin_top: Unit = field(default_factory=lambda: ZERO)
    margin_right: Unit = field(default_factory=lambda: ZERO)
    margin_bottom: Unit = field(default_factory=lambda: ZERO)
    margin_left: Unit = field(default_factory=lambda: ZERO)
    gutter: Unit = field(default_factory=lambda: ZERO)
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

    def make_rotation(self) -> Paper:
        """Create a 90-degree clockwise rotation of this paper.

        The ``gutter`` field is left unchanged.
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

    def modified(
        self,
        width: Optional[Unit] = None,
        height: Optional[Unit] = None,
        margin_top: Optional[Unit] = None,
        margin_right: Optional[Unit] = None,
        margin_bottom: Optional[Unit] = None,
        margin_left: Optional[Unit] = None,
        gutter: Optional[Unit] = None,
    ) -> Paper:
        """Derive a new ``Paper`` from this one with any given changed attributes."""
        return Paper(
            width if width is not None else self.width,
            height if height is not None else self.height,
            margin_top if margin_top is not None else self.margin_top,
            margin_right if margin_right is not None else self.margin_right,
            margin_bottom if margin_bottom is not None else self.margin_bottom,
            margin_left if margin_left is not None else self.margin_left,
            gutter if gutter is not None else self.gutter,
        )


# Templates for common paper types are declared below

A4 = Paper(Mm(210), Mm(297), Mm(20), Mm(20), Mm(20), Mm(20), ZERO)
"""Template for A4-sized portrait paper"""

LETTER = Paper(Inch(8.5), Inch(11), Inch(1), Inch(1), Inch(1), Inch(1), ZERO)
"""Template for letter-sized portrait paper"""
