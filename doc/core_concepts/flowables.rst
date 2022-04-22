Flowable Containers
===================

So far we've discussed how to draw objects with exactly one graphical representation placed fairly literally on a page, but a common feature of musical scores is flowable containers like staff systems. We can imagine flowable containers as long horizontal strips which are broken into different segments as they wrap around the page edges. Objects within these containers may need to be drawn multiple times—and in multiple locations—if they span those breaks.

Neoscore has fairly good support for such notation systems via the :obj:`.Flowable` class and its associated render hooks in :obj:`.PositionedObject` classes. 

.. rendered-example::

    flow = Flowable(ORIGIN, None, Mm(500), Mm(15))
    Text(ORIGIN, flow, "text on first line")
    Text((Mm(200), ZERO), flow, "text on second line")
    Text((Mm(300), ZERO), flow, "text spanning line break")

Objects placed within a flowable are automatically rendered in the flowed space. When an object fits entirely in a given flowed line, it's rendered like usual, just in a different place. Things get more interesting when objects span line breaks. Simple classes like :obj:`.Path` and :obj:`.Text` simply break across the line (clipping at the line edges), but other classes can support special rendering behavior as an object appears in different places relative to flowable breaks by implementing :obj:`.PositionedObject._render_complete`, :obj:`.PositionedObject._render_before_break`, :obj:`.PositionedObject._render_after_break`, and :obj:`.PositionedObject._render_spanning_continuation`. These render calls are dispatched over the span of an object's :obj:`breakable_length <.PositionedObject.breakable_length>`.
    
.. todo::

   Once break hints are implemented updates these docs