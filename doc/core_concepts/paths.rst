Paths
=====

The final fundamental graphical object type is :obj:`.Path`, which allows drawing arbitrary shapes using lines and curves.

.. rendered-example::

   path = Path(ORIGIN, None, "#ff00ff55")
   path.line_to(Mm(10), Mm(-10))
   path.line_to(Mm(20), Mm(0))
   path.line_to(Mm(30), Mm(-10))
   path.cubic_to(Mm(40), Mm(-10), Mm(40), Mm(10), Mm(30), Mm(10))

(The brushes and pens used to fill and outline shapes will be covered in the next section)

Paths are drawn by calling the various drawing methods. :obj:`.Path.line_to` draws a straight line from the current drawing position. :obj:`.Path.cubic_to` similarly draws a `bezier curve <https://en.wikipedia.org/wiki/B%C3%A9zier_curve>`_. :obj:`.Path.move_to` breaks off the current subpath and starts a new one at a given position. :obj:`.Path.close_subpath` connects a line to the current subpath's starting position.

By default, the positions passed to these drawing operations are relative to the path itself. The created path elements can be attached to other objects using the various ``parent`` arguments.

.. rendered-example::

   text = Text((Mm(50), Mm(-10)), None, "a parent")
   path = Path(ORIGIN, None, "#0000ff55")
   path.line_to(Mm(-1), Mm(1), text)
   path.line_to(Mm(-1), Mm(12), text)
   path.close_subpath()


:obj:`.Path` provides several convenience constructors for drawing common shapes including:

* :obj:`.Path.straight_line` (simple 2-point lines)
* :obj:`.Path.rect` (rectangles)
* :obj:`.Path.ellipse` (ellipses and circles)
* :obj:`.Path.arc` (elliptical arcs)
* :obj:`.Path.arrow` (arrows)
