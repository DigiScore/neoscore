#!/usr/bin/env python3

# TODO: Build me

# Imports
import random

from brown.document import Document
from brown.flow import Flow
from brown.staff_system import StaffSystem
from brown.staff import Staff
from brown.note_column import NoteColumn
from brown.units import mm

from brown.lib import instruments

# Set up document
document = Document('letter',  # default paper type
                    margin_top=mm(25),
                    margin_bottom=mm(25),
                    margin_inner=mm(25),
                    margin_outer=mm(25))

# Create a flowable in the document
# Probably make the flow wider ("taller") to give padding for staves
main_flow = Flow(document, 0, 0, mm(1000), mm(96))

# Add a system to the document with two staves
staff_system = StaffSystem(main_flow)
# Verbosity for infrequent statements (like building staves) is OK
# Should staves have a built in instrument property? Or should those be decoupled?
# What if instruments were just thought of purely as bits of repeating text by staves...
v1_staff = Staff(parent_flow=main_flow,
                 starting_x=mm(0),
                 starting_y=mm(0),
                 length=main_flow.length,  # This will be the default value anyway
                 initial_clef='treble',
                 initial_instrument=instruments.Violin)
v2_staff = Staff(parent_flow=main_flow,
                 starting_x=mm(0),
                 starting_y=mm(24),
                 length=main_flow.length,
                 initial_clef='treble',
                 initial_instrument=instruments.Violin)
viola_staff = Staff(parent_flow=main_flow,
                    starting_x=mm(0),
                    starting_y=mm(48),
                    length=main_flow.length,
                    initial_clef='alto',
                 initial_instrument=instruments.Viola)
cello_staff = Staff(parent_flow=main_flow,
                    starting_x=mm(0),
                    starting_y=mm(72),
                    length=main_flow.length,
                    initial_clef='bass',
                 initial_instrument=instruments.Cello)

for staff in [v1_staff, v2_staff, viola_staff, cello_staff]:
    staff_system.add_staff(staff)

# Add special barlines in even intervals
for p in range(0, int(staff_system.length), 50):  # every 50 mm
    staff_system.add_barline(p, style='between-staves', line_style='dash')
# Add some random notes in the staves
for staff in staff_system.staves:
    for i in range(100):
        staff.add_notecolumn(x_pos=random.randint(0, staff.total_length),
                             pitches=random.randint(-8, 8))

# Export the document to SVG and PNG
document.save_as_svg('vector_output.svg')
document.save_as_png('image_output.png')

