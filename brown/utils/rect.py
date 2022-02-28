from __future__ import annotations

from dataclasses import dataclass

from brown.utils.units import Unit


@dataclass(frozen=True)
class Rect:
    """A rectangle data class.

    The `x` and `y` coordinates represent the starting position,
    typically the top left corner. `width` and `height` extend
    rightward and downward.
    """

    x: Unit
    y: Unit
    width: Unit
    height: Unit
