from examples.feldman_projections_2.content import instruments
from examples.feldman_projections_2.grid_unit import GridUnit
from examples.feldman_projections_2.score import Score
from neoscore.core import neoscore

neoscore.setup()

# flowable = Flowable((GridUnit(0), GridUnit(0)), Measure(100), GridUnit(10))
score = Score((GridUnit(0), GridUnit(0)), None, instruments)

neoscore.show()
