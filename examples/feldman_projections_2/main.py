from examples.feldman_projections_2.content import instruments
from examples.feldman_projections_2.grid_unit import GridUnit
from examples.feldman_projections_2.measure import Measure
from examples.feldman_projections_2.score import Score
from neoscore.core import neoscore
from neoscore.core.flowable import Flowable
from neoscore.core.paper import A4
from neoscore.core.point import ORIGIN

neoscore.setup(A4)

flowable = Flowable(
    ORIGIN,
    None,
    Measure(20),
    GridUnit(18),
    GridUnit(6),
    Measure(1),
)
score = Score(ORIGIN, flowable, instruments)

neoscore.show()
