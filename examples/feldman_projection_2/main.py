"""The main entrypoint for the example score."""

import math

from examples.feldman_projection_2.content_no2 import instruments
from examples.feldman_projection_2.grid_unit import GridUnit
from examples.feldman_projection_2.measure import Measure
from examples.feldman_projection_2.score import Score
from examples.helpers import render_example
from neoscore.core import neoscore
from neoscore.core.flowable import Flowable
from neoscore.core.paper import LETTER
from neoscore.core.point import ORIGIN

# Init neoscore in landscape mode
neoscore.setup(LETTER.make_rotation())

# Calculate the number of measures needed for the score-containing flowable
last_event_pos: GridUnit = GridUnit(0)
for instrument in instruments:
    for event in instrument.event_data:
        last_event_pos = max(last_event_pos, event.pos_x)
measure_count = math.ceil(Measure(last_event_pos).display_value)

# Construct flowable with needed dimensions
flowable = Flowable(
    ORIGIN,
    None,
    Measure(measure_count),
    GridUnit(18),
    GridUnit(6),
    Measure(2),
)
# Init score
score = Score(ORIGIN, flowable, instruments)

# Render
render_example("feldman")

# For PDF output, replace the above line with:
# neoscore.render_pdf(output_path)
