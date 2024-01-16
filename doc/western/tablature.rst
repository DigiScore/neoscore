Tablature
=========

Neoscore offers a few classes to facilitate writing tabs. The built-in functionality was mostly written with guitar tabs in mind, but should serve other tablature needs as well.

Tabs can be written with the dedicated staff and clef types, :obj:`.TabStaff` and :obj:`.TabClef`.

.. rendered-example::

   staff = TabStaff(ORIGIN, None, Mm(50))
   # Tab clefs are purely cosmetic and they don't take a start position
   TabClef(staff)  

Significantly, tab staves typically have a wider line spacing than conventional staves, and by default their font is sized such that ``tab_staff.unit(1)`` is 2/3 the line spacing.

.. rendered-example::

   staff = TabStaff(ORIGIN, None, Mm(50))
   TabClef(staff)
   MusicText((ZERO, staff.unit(3)), staff, 'noteheadBlack')

The font and line spacing can be independently set using constructor arguments.

.. rendered-example::

   staff = TabStaff(ORIGIN, None, Mm(50), music_font=MusicFont("Bravura", Mm(2)))
   TabClef(staff)
   MusicText((ZERO, staff.unit(3)), staff, 'noteheadBlack')

In this system, staff positions no longer neatly correspond to multiples of ``staff.unit(0.5)``, so you'll want to use :obj:`.TabStaff.string_y` to find positions.

.. rendered-example::

   staff = TabStaff(ORIGIN, None, Mm(50))
   TabClef(staff)
   MusicText((ZERO, staff.string_y(5)), staff, 'noteheadBlack')

Of course, you probably won't be using noteheads in your tablature! As in any other context, you can place most neoscore objects in tab staves. For the common use-case of placing musical text on staff lines we provide :obj:`.TabStringText`, a :obj:`.MusicText` centered on a line number which by default hides its background.

.. rendered-example::

   staff = TabStaff(ORIGIN, None, Mm(50))
   TabClef(staff)
   # 2 is the line/string number
   TabStringText(ZERO, staff, 2, "guitarShake", alignment_x=AlignmentX.LEFT)

For the common use-case of putting numbers on lines, like fret numbers in guitar tabs, we provide a specialized :obj:`.TabNumber` class which just takes a string/line number and a number to write.

.. rendered-example::

   staff = TabStaff(ORIGIN, None, Mm(50), line_count=4)
   TabClef(staff)
   TabNumber(Mm(0), staff, 1, 5)
   TabNumber(Mm(5), staff, 2, 10)  # Multi-digit numbers work too
   TabNumber(Mm(10), staff, 3, 7)
   TabNumber(Mm(15), staff, 4, 10)
   # Chords can be written by simply stacking TabNumbers.
   TabNumber(Mm(20), staff, 2, 1)
   TabNumber(Mm(20), staff, 3, 1)
