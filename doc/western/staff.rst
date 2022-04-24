Staff
=====

Staves can be created just like any other object.

.. rendered-example::

   Staff(ORIGIN, None, Mm(100))

Staves can be made to wrap around page edges by placing them in flowable containers.

.. rendered-example::

   flowable = Flowable(ORIGIN, None, Mm(300), Mm(30))
   Staff(ORIGIN, flowable, Mm(300))

Each staff has an associated :obj:`.MusicFont` whose :obj:`unit <.MusicFont.unit>` encodes the distance between two staff lines.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   Text((Mm(0), staff.music_font.unit(1)), staff, "text on second staff line")

Staves support customization out of the box; they can be any size, have any number of lines, and they can be drawn with different pens.

.. rendered-example::

   Staff(ORIGIN, None, Mm(100))
   Staff((ZERO, Mm(15)), None, Mm(100), line_spacing=Mm(1))
   Staff((ZERO, Mm(30)), None, Mm(100), line_count=1)
   Staff((ZERO, Mm(45)), None, Mm(100), line_count=3)
   Staff((ZERO, Mm(60)), None, Mm(100), line_count=8)
   Staff((ZERO, Mm(85)), None, Mm(100), pen=Pen("#ff0000", pattern=PenPattern.DASH))