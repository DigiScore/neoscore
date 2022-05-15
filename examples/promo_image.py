import itertools
import random

from helpers import render_example

from neoscore.core import flowable, neoscore
from neoscore.core.brush import Brush
from neoscore.core.color import Color, ColorDef
from neoscore.core.directions import DirectionY
from neoscore.core.flowable import Flowable
from neoscore.core.music_text import MusicText
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Mm, Unit
from neoscore.western.clef import Clef
from neoscore.western.pitch import Pitch, PitchDef
from neoscore.western.slur import Slur
from neoscore.western.staff import Staff
from neoscore.western.staff_group import StaffGroup
from neoscore.western.staff_object import StaffObject
from neoscore.western.system_line import SystemLine

neoscore.setup()

flowable = Flowable(ORIGIN, None, Mm(4000), Mm(75))
group = StaffGroup()
staff_1 = Staff(ORIGIN, flowable, Mm(2000), group, line_count=8)
staff_2 = Staff((ZERO, Mm(25)), flowable, Mm(2000), group)

perc_clef = Clef(ZERO, staff_1, "percussion_1")
bass_clef = Clef(ZERO, staff_2, "bass_8vb")

SystemLine(group)

wiggle_glyph_sizes = ["Smallest", "Small", "Medium", "Large", "Largest"]
wiggle_glyph_speeds = ["Fastest", "FasterStill", "Fast", "Slow", "Slower", "Slowest"]
all_wiggle_vibrato_glyphs = [
    f"wiggleVibrato{size}{speed}"
    for size, speed in itertools.product(wiggle_glyph_sizes, wiggle_glyph_speeds)
]
# Remove 2 glyphs missing in Bravura (https://github.com/steinbergmedia/bravura/issues/70)
all_wiggle_vibrato_glyphs.remove("wiggleVibratoMediumSlower")
all_wiggle_vibrato_glyphs.remove("wiggleVibratoLargestSlower")
all_random_wiggle_glyphs = [f"wiggleRandom{n}" for n in range(1, 5)]
all_wiggle_glyphs = all_wiggle_vibrato_glyphs + all_random_wiggle_glyphs

next_x = ZERO
for i in range(50):
    y = staff_1.unit(random.randint(0, 7))
    text_len = random.randint(1, 15)
    wiggle_object_glyphs = random.choices(all_wiggle_glyphs, k=text_len)
    mtext = MusicText((next_x, y), staff_1, wiggle_object_glyphs, z_index=10)
    # Hide staff just around the text path by duplicating the text with a thick white pen
    # Unlike setting a background brush, this trick only hides things right around the text
    MusicText(
        ORIGIN,
        mtext,
        mtext.music_chars,
        brush=Brush.no_brush(),
        pen=Pen(neoscore.background_brush.color, staff_1.unit(1)),
        z_index=mtext.z_index - 1,
    )
    next_x += mtext.bounding_rect.width + staff_1.unit(random.randint(0, 5))


class BlockNote(PositionedObject, StaffObject):
    def __init__(
        self,
        pos_x: Unit,
        staff: Staff,
        pitch: PitchDef,
        length: Unit,
        color: ColorDef = "000",
    ):
        pitch = Pitch.from_def(pitch)
        pitch_y = staff.middle_c_at(pos_x) + staff.unit(pitch.staff_pos_from_middle_c)
        PositionedObject.__init__(self, (pos_x, pitch_y), staff)
        StaffObject(staff)
        self.length = length
        height = staff.unit(1)
        Path.rect((ZERO, height / -2), self, length, height, Brush(color), Pen.no_pen())


colors = ["#1C5253", "#C3EB78", "#B6174B"]
blocks = []
for i in range(100):
    x = Unit(random.uniform(0, staff_1.breakable_length.base_value))
    length = staff_1.unit(random.randint(1, 20))
    pitch = Pitch(random.choice("abcdefg"), None, random.randint(1, 2))
    base_color = Color.from_def(random.choice(colors))
    color = Color(
        base_color.red, base_color.green, base_color.blue, random.randint(55, 255)
    )
    blocks.append(BlockNote(x, staff_2, pitch, length, color))

# Add some slurs between blocks
blocks.sort(key=lambda b: b.x)
for i in range(20):
    start_i = random.randint(0, len(blocks) - 2)
    end_i = min(len(blocks) - 1, start_i + random.randint(1, 3))
    start_block = blocks[start_i]
    end_block = blocks[end_i]
    direction = DirectionY.DOWN if start_block.y > staff_2.center_y else DirectionY.UP
    y_offset = staff_2.unit(3 * direction.value)
    slur = Slur(
        (ZERO, y_offset),
        start_block,
        (end_block.length, y_offset),
        end_block,
        direction,
    )

render_example("promo_image")
