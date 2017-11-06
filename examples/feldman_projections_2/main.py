from brown.core import brown

from examples.feldman_projections_2.content import content
from examples.feldman_projections_2.grid_unit import GridUnit
from examples.feldman_projections_2.score import Score

brown.setup()

score = Score((GridUnit(0), GridUnit(0)), content)

brown.show()
