Expressive Text
===============

Expressive text markings like dynamics and tempo marks can be written using simple :obj:`.Text` and :obj:`.MusicText` objects, but in some cases we provide built-in classes for convenience.

Dynamics
--------

Classical dynamics can be easily written in their idiomatic style with the :obj:`.Dynamic` class.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(30))
   Dynamic((ZERO, staff.unit(7)), staff, "p")

Dynamic strings can consist of any of the following letters: `p, m, f, r, s, z, n`.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(30))
   Dynamic((ZERO, staff.unit(7)), staff, "sfz")

Metronome Markings
------------------

.. todo::

    These aren't easily supported yet. See `#19 <https://github.com/DigiScore/neoscore/issues/19>`_.