Rotation and Scaling
====================

Neoscore has partial support for object rotation and scaling.

.. rendered-example::

   Text(ORIGIN, None, "Rotation!", rotation=70)
   Text((Mm(30), ZERO), None, "Scaling!", scale=2)

All graphical objects can be scaled and rotated. When the fields aren't available in the constructor, they can be set after init with properties.

Rotation values are specified in clockwise degrees. Scale values are specified in scaling factors, where 1 is no scaling. By default these operations are performed relative to the object's local origin, but this can be overridden with the :obj:`transform_origin <.PositionedObject.transform_origin>` field.

Both of these transforms are inherited by children *outside flowable contexts*.

.. rendered-example::

   parent = Text(ORIGIN, None, "parent", rotation=-45, scale=1.2)
   Text((Mm(20), Mm(10)), parent, "child", rotation=10)
   
.. rendered-example::

   prev = Text((ZERO, Mm(20)), None, "root")

   for i in range(1, 5):
       prev = Text((Mm(20), ZERO), prev, f"desc_{i}", scale=1.1, rotation=5)

But note that within flowables, these transforms are not inherited.

.. rendered-example::

   flowable = Flowable(ORIGIN, None, Mm(200), Mm(15))
   parent = Text(ORIGIN, flowable, "parent", rotation=-45, scale=1.2)
   Text((Mm(20), Mm(10)), parent, "child", rotation=10)

Caveats
-------

Support for these features is experimental and incomplete, especially within flowable contexts. :obj:`.Path`\ s which have elements parented to other objects do not display correctly when rotated. Rotated objects also do not display correctly when they cross :obj:`.Flowable` line breaks.

You can find a more thorough `description of known shortcomings of rotation in Issue #9 <https://github.com/DigiScore/neoscore/issues/9>`_.
