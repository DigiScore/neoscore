Tablature
=========

Neoscore offers a classes to facilitate writing tabs. The built-in functionality was mostly written with guitar tabs in mind, but should serve other tablature needs as well.

Tabs can be written with the dedicated staff and clef types, :obj:`.TabStaff` and :obj:`.TabClef`.

.. rendered-example::

   staff = TabStaff(ORIGIN, None, Mm(50))
   TabClef(ZERO, staff)  # Tab clefs are purely cosmetic

Tab staves have a few important differences from conventionaly ones. Tab staves typically have a wider line spacing than conventionally staves, and by default their font is sized such that ``tab_staff.unit(1)`` is 2/3 the line spacing.

.. rendered-example::

   staff = TabStaff(ORIGIN, None, Mm(50))
   TabClef(ZERO, staff)
   MusicText((staff.unit(5), staff.unit(3)), staff, 'noteheadBlack')

The font and line spacing can be independently set using constructor arguments.

.. rendered-example::

   staff = TabStaff(ORIGIN, None, Mm(50), music_font=MusicFont("Bravura", Mm(2)))
   TabClef(ZERO, staff)
   MusicText((staff.unit(5), staff.unit(3)), staff, 'noteheadBlack')

In this system, staff positions no longer neatly correspond to multiples of ``staff.unit(0.5)``, so you'll want to use :obj:`.TabStaff.string_y` to find positions.

.. rendered-example::

   staff = TabStaff(ORIGIN, None, Mm(50))
   TabClef(ZERO, staff)
   MusicText((Mm(10), staff.string_y(5)), staff, 'noteheadBlack')

Of course, you probably won't be using noteheads in your tablature! Like any other context, you can place most neoscore objects in tabs. For the common use-case of placing musical text on staff lines we provide :obj:`.TabStringText`, a centered :obj:`.MusicText` which by default hides its background.

.. rendered-example::

   staff = TabStaff(ORIGIN, None, Mm(50))
   TabClef(ZERO, staff)
   TabStringText(Mm(10), staff, 2, "guitarShake")  # 2 is the string number

For the common use-case of putting numbers on lines, like fret numbers in guitar tabs, we provide a specialized :obj:`.TabNumber` class which just takes a string and a number to write.

.. rendered-example::

   staff = TabStaff(ORIGIN, None, Mm(50), line_count=4)
   TabClef(ZERO, staff)
   TabNumber(Mm(10), staff, 1, 5)
   TabNumber(Mm(15), staff, 2, 10)  # Multi-digit numbers work too
   TabNumber(Mm(20), staff, 3, 7)
   TabNumber(Mm(25), staff, 4, 10)
   # Chords can be written by simply stacking TabNumbers.
   TabNumber(Mm(30), staff, 2, 1)
   TabNumber(Mm(30), staff, 3, 1)