Rotation and Scaling
====================

Neoscore has partial support for object rotation and scaling.

.. rendered-example::

   Text(ORIGIN, None, "Rotation!", rotation=70)
   Text((Mm(30), ZERO), None, "Scaling!", scale=2)

All simple objects can be scaled and rotated with arguments or properties like these, with the exception of :obj:`.Path`, which does not support scaling.

Rotation values are specified in clockwise degrees. Scale values are specified in scaling factors. Both operations are performed relative to the object's local origin.

Caveats
-------

These features have many caveats. Most significantly, rotation and scaling do not propogate to object children. This means compound objects containing others (encompassing many of the :obj:`.western` module's objects) cannot be rotated or scaled together.

.. rendered-example::

   parent = Text(ORIGIN, None, "Transformed parent", rotation=-45, scale=1.5)
   Text((Mm(20), Mm(10)), parent, "Children are unaffected")

Furthermore, this means that :obj:`.Path`\ s which have elements parented to other objects do not display correctly when rotated.

Rotated objects also do not display correctly when they cross :obj:`.Flowable` line breaks. You can find a more thorough `description of known shortcomings of rotation in Issue #9 <https://github.com/DigiScore/neoscore/issues/9>`_.