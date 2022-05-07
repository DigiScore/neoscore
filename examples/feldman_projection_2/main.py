"""The main entrypoint for the example score."""

from examples.feldman_projection_2.content import instruments
from examples.feldman_projection_2.grid_unit import GridUnit
from examples.feldman_projection_2.measure import Measure
from examples.feldman_projection_2.score import Score
from neoscore.core import neoscore
from neoscore.core.flowable import Flowable
from neoscore.core.paper import LETTER
from neoscore.core.point import ORIGIN

neoscore.setup(LETTER.make_rotation())

flowable = Flowable(
    ORIGIN,
    None,
    Measure(20),
    GridUnit(18),
    GridUnit(6),
    Measure(2),
)
score = Score(ORIGIN, flowable, instruments)

neoscore.show(display_page_geometry=True)
