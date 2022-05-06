from helpers import render_example

from neoscore.common import *

neoscore.setup()

expressive_font = Font("Lora", Mm(4), italic=True)

flowable = Flowable((Mm(0), Mm(0)), None, Mm(500), Mm(30), Mm(10), Mm(20))
# Indent first line
flowable.provided_controllers.add(MarginController(ZERO, Mm(20)))
flowable.provided_controllers.add(MarginController(Mm(1), ZERO))

staff_group = StaffGroup()
upper_staff = Staff((Mm(0), Mm(0)), flowable, Mm(500), staff_group)
lower_staff = Staff((Mm(0), Mm(20)), flowable, Mm(500), staff_group)
staves = [upper_staff, lower_staff]
Brace(Mm(0), staves)
SystemLine(Mm(0), staves)

# We can use the same unit in the upper and lower staves since they
# are the same size
unit = upper_staff.unit

upper_clef = Clef(unit(0), upper_staff, "treble")
lower_clef = Clef(unit(0), lower_staff, "bass")

KeySignature(ZERO, upper_staff, "g_major")
KeySignature(ZERO, lower_staff, "g_major")

TimeSignature(ZERO, upper_staff, (3, 4))
TimeSignature(ZERO, lower_staff, (3, 4))

Dynamic((unit(7), unit(6)), upper_staff, "p")
Text((unit(10), unit(6)), upper_staff, "dolce", expressive_font)

# BAR 1 ###################################################

# Upper staff notes
Chordrest(unit(8), upper_staff, ["g'"], Duration(1, 4))
Chordrest(unit(12), upper_staff, ["g'"], Duration(1, 4))
a = Chordrest(unit(16), upper_staff, ["a'"], Duration(3, 16))
MusicText((unit(-1), unit(-2)), a, "ornamentMordent")
b = Chordrest(unit(19), upper_staff, ["b'"], Duration(1, 16))
BeamGroup([a, b])

# Lower staff notes - upper voice
Chordrest(unit(10), lower_staff, None, (1, 4), unit(-3))
Chordrest(unit(16), lower_staff, ["d"], Duration(1, 4), stem_direction=DirectionY.UP)

# Lower staff notes - middle voice
Chordrest(unit(8), lower_staff, None, (1, 4), rest_y=unit(-2))
Chordrest(unit(12), lower_staff, ["b,"], Duration(2, 4), stem_direction=DirectionY.UP)

# Lower staff notes - lower voice
Chordrest(unit(8), lower_staff, ["g,"], Duration(3, 4))

Barline(unit(22), staves)

# BAR 2 ###################################################

b2 = unit(23)

# Upper staff notes
a = Chordrest(b2, upper_staff, ["a'"], (1, 8))
b = Chordrest(b2 + unit(3), upper_staff, ["f'"], (1, 8))
Chordrest(b2 + unit(6), upper_staff, ["d'"], (1, 2))
BeamGroup([a, b])
# grace notes should be used here, but they aren't supported yet

# Lower staff notes (same pattern as prev bar)

# Lower staff notes - upper voice
Chordrest(b2 + unit(4), lower_staff, None, (1, 4), rest_y=unit(-3))
Chordrest(
    b2 + unit(9),
    lower_staff,
    ["d"],
    Duration(1, 4),
    stem_direction=DirectionY.UP,
)

# Lower staff notes - middle voice
Chordrest(b2, lower_staff, None, (1, 4), rest_y=unit(-2))
Chordrest(
    b2 + unit(6),
    lower_staff,
    ["a,"],
    Duration(2, 4),
    stem_direction=DirectionY.UP,
)

# Lower staff notes - lower voice
Chordrest(b2, lower_staff, ["f,"], Duration(3, 4))


# Barline to test line breaking
Barline(Mm(140), staves)
render_example("goldberg")
