from helpers import render_vtest

from neoscore.common import *

neoscore.setup()

expressive_font = Font("Lora", Mm(4), italic=True)

flowable = Flowable((Mm(0), Mm(0)), None, Mm(500), Mm(30), Mm(10))

upper_staff = Staff((Mm(0), Mm(0)), flowable, Mm(500))
lower_staff = Staff((Mm(0), Mm(20)), flowable, Mm(500))
Brace(Mm(0), [upper_staff, lower_staff])

# We can use the same unit in the upper and lower staves since they
# are the same size
unit = upper_staff.unit

upper_clef = Clef(unit(0), upper_staff, "treble")
lower_clef = Clef(unit(0), lower_staff, "bass")

# Once flowable gutters are implemented, this explicit offsets for
# key/time sigs will not be needed
KeySignature(upper_clef.bounding_rect.width + unit(0.5), upper_staff, "g_major")
KeySignature(lower_clef.bounding_rect.width + unit(0.5), lower_staff, "g_major")

TimeSignature(unit(5), upper_staff, (3, 4))
TimeSignature(unit(5), lower_staff, (3, 4))

Dynamic((unit(7), unit(6)), upper_staff, "p")
Text((unit(10), unit(6)), upper_staff, "dolce", expressive_font)

# Upper staff notes
Chordrest(unit(8), upper_staff, ["g''"], Duration(1, 4))
Chordrest(unit(12), upper_staff, ["g''"], Duration(1, 4))
a = Chordrest(unit(16), upper_staff, ["a''"], Duration(3, 16))
MusicText((unit(-1), unit(-2)), a, "ornamentMordent")
Chordrest(unit(19), upper_staff, ["b''"], Duration(1, 16))

# Lower staff notes - upper voice
Rest(Point(unit(10), unit(-3)), lower_staff, Duration(1, 4))
Chordrest(
    unit(16), lower_staff, ["d'"], Duration(1, 4), stem_direction=VerticalDirection.UP
)

# Lower staff notes - middle voice
# Can't use Chordrest for these rests because Chordrest doesn't
# currently support explicit vertical positioning of rests.
Rest(Point(unit(8), unit(-2)), lower_staff, Duration(1, 4))
Chordrest(
    unit(12), lower_staff, ["b"], Duration(2, 4), stem_direction=VerticalDirection.UP
)

# Lower staff notes - lower voice
Chordrest(unit(8), lower_staff, ["g"], Duration(3, 4))

Barline(unit(22), [upper_staff, lower_staff])

render_vtest("goldberg")
