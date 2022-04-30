Multi-Staff Objects
===================

Some objects, like barlines and braces, span multiple staves. Such classes inherit :obj:`.MultiStaffObject`, and the general pattern for creating them is to pass a complete list of the staves spanned in descending order.

Barlines
--------

Barlines can be easily created with the :obj:`.Barline` class.

.. rendered-example::

   staff_1 = Staff(ORIGIN, None, Mm(40))
   staff_2 = Staff((ZERO, Mm(15)), None, Mm(40))
   staves = [staff_1, staff_2]
   Barline(Mm(20), staves)

A couple common barline types are built-in, and available via constants in the :obj:`.barline_style` module.

.. rendered-example::

   staff_1 = Staff(ORIGIN, None, Mm(40))
   staves = [staff_1]
   Barline(Mm(20), staves, barline_style.SINGLE)  # The default
   Barline(Mm(30), staves, barline_style.THIN_DOUBLE)
   Barline(Mm(40), staves, barline_style.END)

Custom styles can be defined by providing a list of :obj:`.BarlineStyle`\ s.

.. rendered-example::

   staff_1 = Staff(ORIGIN, None, Mm(40))
   staff_2 = Staff((ZERO, Mm(15)), None, Mm(40))
   staves = [staff_1, staff_2]
   styles = [
       BarlineStyle(thickness=0.5, gap_right=1.5),
       BarlineStyle(thickness=0.3, gap_right=1, color="#ff0000"),
       BarlineStyle(pattern=PenPattern.DASH, color="#3300ff"),
   ]
   Barline(Mm(20), staves, styles)

The position passed to :obj:`.Barline` is used as the `right edge` of the barline, including adjustments for thickness. This allows you to easily align ending barlines with staff ends.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(40))
   Barline(Mm(40), [staff], barline_style.END)

By default, barlines which extend across multiple staves are fully connected. This can be changed so the barline breaks between staves with the ``connected`` argument.

.. rendered-example::

   staff_1 = Staff(ORIGIN, None, Mm(40))
   staff_2 = Staff((ZERO, Mm(15)), None, Mm(40))
   staves = [staff_1, staff_2]
   Barline(Mm(20), staves, connected=False)

Barlines automatically attach a :obj:`.BreakHint` immediately after them, so if they're placed in a flowable they can suggest line break opportunities.

.. rendered-example::

   import random
   flowable = Flowable(ORIGIN, None, Mm(400), Mm(15), break_threshold=Mm(30))
   staff = Staff(ORIGIN, flowable, Mm(400))
   x = Mm(20)
   while x < Mm(400):
       Barline(x, [staff])
       x += Mm(random.randint(20, 50))

.. todo::

    This currently doesn't work well, but should be fixed before release

Braces
------

Staff system braces can be created with the :obj:`.Brace` class. Braces are automatically right-aligned to their given position and they appear at the beginning of every staff system after their placement.

.. rendered-example::

   staff_1 = Staff(ORIGIN, None, Mm(40))
   staff_2 = Staff((ZERO, Mm(15)), None, Mm(40))
   staves = [staff_1, staff_2]
   Brace(ZERO, staves)

.. rendered-example::

   flowable = Flowable(ORIGIN, None, Mm(400), Mm(30))
   staff_1 = Staff(ORIGIN, flowable, Mm(400))
   staff_2 = Staff((ZERO, Mm(15)), flowable, Mm(400))
   Brace(ZERO, [staff_1, staff_2])

