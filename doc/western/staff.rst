Staves, Clefs, and Signatures
=============================

Staves can be created just like any other object.

.. rendered-example::

   Staff(ORIGIN, None, Mm(100))

Staves can be made to wrap around page edges by placing them in flowable containers.

.. rendered-example::

   flowable = Flowable(ORIGIN, None, Mm(300), Mm(30))
   Staff(ORIGIN, flowable, Mm(300))

Each staff has an associated :obj:`unit <.Staff.unit>` type which encodes the distance between two staff lines.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   Text((Mm(0), staff.unit(1)), staff, "text on second staff line")

Staves support customization out of the box; they can be any size, have any number of lines, and they can be drawn with different pens.

.. rendered-example::

   Staff(ORIGIN, None, Mm(100))
   Staff((ZERO, Mm(15)), None, Mm(100), line_spacing=Mm(1))
   Staff((ZERO, Mm(30)), None, Mm(100), line_count=1)
   Staff((ZERO, Mm(45)), None, Mm(100), line_count=3)
   Staff((ZERO, Mm(60)), None, Mm(100), line_count=8)
   Staff((ZERO, Mm(85)), None, Mm(100), pen=Pen("#ff0000", pattern=PenPattern.DASH))


Clefs
-----

:obj:`.Clef`\ s control staff pitch layout. They're automatically drawn once wherever placed, and then at the beginning of every subsequent staff system until another clef is encountered. Initial clefs should be placed at ``ZERO`` for proper fringe layout.

.. rendered-example::

    flowable = Flowable(ORIGIN, None, Mm(400), Mm(15))
    staff = Staff(ORIGIN, flowable, Mm(400))
    Clef(ZERO, staff, 'treble')
    Clef(Mm(250), staff, 'bass')

Several common clef types are built in, and for convenience these can be specified by their string names. These include:

* ``'treble'``
* ``'treble_8vb'``
* ``'treble_8va'``
* ``'bass'``
* ``'bass_8vb'``
* ``'tenor'``
* ``'alto'``
* ``'percussion_1'``
* ``'percussion_2'``
* ``'bridge'``

Custom clefs can also be defined using arbitrary glyphs and pitch offsets using :obj:`.ClefType`.

Key Signatures
--------------

Cosmetic standard key signatures are supported out of the box. Like clefs, they are automatically drawn once where placed and then at every subsequent line until canceled by another. Initial signatures should also be placed at ``ZERO``.

.. rendered-example::

   flowable = Flowable(ORIGIN, None, Mm(300), Mm(15))
   staff = Staff(ORIGIN, flowable, Mm(300))
   Clef(ZERO, staff, 'treble')
   KeySignature(ZERO, staff, 'gf_major')

.. note::

   Key signatures must be placed at a point in the staff with an active clef. Note also that key signatures are purely cosmetic and have no effect on how note accidentals are written.

Key signature types can be given as string shorthands of the form ``[pitch letter][f|s]_[major|minor]``, for example ``'c_major'``, ``'fs_minor'``, or ``'df_major'``. You can also specify enum variants of :obj:`.KeySignatureType`.

Time Signatures
---------------

Time signatures can also be attached to staves, again using ``ZERO`` for initial placement for proper fringe layout.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   TimeSignature(ZERO, staff, (4, 4))

Meters can be defined in a few different ways. A 2-tuple as seen above will give a simple two-number signature. You can also specify additive signatures by passing a list in the upper number. The special glyphs for "common" and "cut" time can be specified using :obj:`.COMMON_TIME` and :obj:`.CUT_TIME`. Arbitrary glyphs can also be used by directly creating :obj:`.Meter` objects.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   TimeSignature(ZERO, staff, (3, 16))
   TimeSignature(Mm(20), staff, ([3, 3, 2], 8))
   TimeSignature(Mm(50), staff, COMMON_TIME)
   TimeSignature(Mm(70), staff, Meter(['accidentalSharp'], ['accidentalFlat']))


.. note::

   Time signatures are purely cosmetic since neoscore's limited engraving knowledge is not meter-aware.

Instrument Names
----------------

Instrument names can be drawn to the left of staff systems using the :obj:`.InstrumentName` class. It draws text right-aligned and vertically centered at a given position relative to the top left corner of each staff fringe. You can optionally provide is a different string to use for lines after the first, including a blank string to leave later lines blank.

.. rendered-example::

   flowable = Flowable(ORIGIN, None, Mm(300), Mm(15))
   staff = Staff(ORIGIN, flowable, Mm(300))
   InstrumentName((staff.unit(-2), staff.center_y), staff, "Melodica", "mel")
   Clef(ZERO, staff, 'treble')

Staff Fringes
-------------

Staves are positioned by the start of their live area, just to the right of the "fringe" which contains clefs, key signatures, and so on. When placed in a flowable, staves automatically modify the flowable's margin such that the fringe is placed in the flowable margin and the proper flowable space is occupied by actual objects placed in the staff.

.. rendered-example::

   flowable = Flowable(ORIGIN, None, Mm(300), Mm(15))
   staff = Staff(ORIGIN, flowable, Mm(300))
   Clef(ZERO, staff, 'treble')
   KeySignature(ZERO, staff, 'gf_major')
   TimeSignature(ZERO, staff, ([3, 3, 2], 8))
   Text(ORIGIN, staff, "Staff's local origin is to the right of the fringe "
      + "and flowable space skips over fringes")

Staff Groups
------------

Systems of multiple staves should be connected with each other by a :obj:`.StaffGroup`. This allows their fringes to be aligned in situations where individual staves' fringes have differing sizes.

.. rendered-example::

   length = Mm(300)
   flowable = Flowable(ORIGIN, None, length, Mm(30))
   group = StaffGroup()

   staff_1 = Staff(ORIGIN, flowable, length, group)
   Clef(ZERO, staff_1, "treble")
   KeySignature(ZERO, staff_1, "cf_major")
   TimeSignature(ZERO, staff_1, ([3, 3, 2], 8))

   staff_2 = Staff((ZERO, Mm(15)), flowable, length, group, line_count=1)
   Clef(ZERO, staff_2, "percussion_1")
   TimeSignature(ZERO, staff_2, ([3, 3, 2], 8))

   Text(ORIGIN, staff_2, "Fringe is aligned across staves sharing a StaffGroup")
