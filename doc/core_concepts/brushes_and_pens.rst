Brushes and Pens
================

Both :obj:`.Text` and :obj:`.Path` objects are drawn using :obj:`.Brush`\ es and :obj:`.Pen`\ s.  :obj:`.Brush`\ es control how shapes are filled while :obj:`.Pen`\ s control shape outlines.

.. rendered-example::

   brush = Brush("#ffff0099")
   pen = Pen("000000", Mm(1), PenPattern.DASH)
   Path.rect(ORIGIN, None, Mm(20), Mm(20), brush, pen)


Brushes consist of just a color and an optional :obj:`pattern <.BrushPattern>`.

Pens have a color, a thickness, a line pattern, a join style controlling how line joints are drawn, and a cap style controlling how line ends are drawn.

.. rendered-example::
   
   pens = [
       Pen(thickness=Mm(0.5), pattern=PenPattern.SOLID),
       Pen(thickness=Mm(0.5), pattern=PenPattern.DASH),
       Pen(thickness=Mm(0.5), pattern=PenPattern.DOT),
       Pen(thickness=Mm(0.5), pattern=PenPattern.DASHDOT),
       Pen(thickness=Mm(0.5), pattern=PenPattern.DASHDOTDOT),
   ]

   for i, pen in enumerate(pens):
       Path.straight_line((ZERO, Mm(5 * i)), None, (Mm(40), ZERO), pen=pen)

A pen's thickness controls the overall line thickness measured perpendicular to the drawn line. The true line path always lies in the middle of the drawn stroke. Pens of zero thickness have a special meaning: they are 1 pixel wide regardless of zoom level in interactive views.

..
   This example has to be skipped due to https://github.com/DigiScore/neoscore/issues/14

   .. rendered-example::

      thick_pen = Pen("000000aa", Mm(0.2))
      cosmetically_thin_pen = Pen("#ff0000", ZERO)
      Path.straight_line(ORIGIN, None, (Mm(40), ZERO), pen=thick_pen)
      Path.straight_line(ORIGIN, None, (Mm(40), ZERO), pen=cosmetically_thin_pen)

Sometimes you don't want a brush or a pen. This can be done using the special :obj:`.Brush.no_brush()` and :obj:`.Pen.no_pen()` methods.

.. rendered-example::

   Path.rect(ORIGIN, None, Mm(20), Mm(10), Brush.no_brush())
   Text((Mm(25), Mm(5)), None, "Outline", brush=Brush.no_brush(), pen="#000000")
      
In most places where a brush or pen is needed, you can pass in a color string instead for a solid brush or pen of that color.

.. rendered-example::

   Path.rect(ORIGIN, None, Mm(20), Mm(10), "#ffff0099", "ff00ff")


Colors
------

Neoscore supports 8-bit RGBA :obj:`.Color`\ s. You can construct colors explicitly, but in most situations you can pass CSS-style hex strings wherever a :obj:`.Color` is needed. ::

  >>> Color('#ff0000')
  Color(255, 0, 0, 255)
  >>> Color('#ff0000aa')
  Color(255, 0, 0, 170)

For those unfamiliar with CSS colors, these values represent red, green, blue, and alpha (transparency) channels, each valued 0-255. The shorthand string is a hexadecimal value where each 2-character group after the hash is a hexadecimal number 0-255.

