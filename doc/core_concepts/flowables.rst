Flowable Containers
===================

So far we've discussed how to draw objects with exactly one graphical representation placed fairly literally on a page, but a common feature of musical scores is flowable containers like staff systems. We can imagine flowable containers as long horizontal strips which are broken into different segments as they wrap around the page edges. Objects within these containers may need to be drawn multiple times—and in multiple locations—if they span those breaks.

Neoscore has fairly good support for such notation systems via the :obj:`.Flowable` class and its associated render hooks in :obj:`.PositionedObject` classes.

.. rendered-example::

    flow = Flowable(ORIGIN, None, Mm(500), Mm(15))
    Text(ORIGIN, flow, "text on first line")
    Text((Mm(200), ZERO), flow, "text on second line")
    Text((Mm(300), ZERO), flow, "text spanning line break")

Objects placed within a flowable are automatically rendered in the flowed space. When an object fits entirely in a given flowed line, it's rendered like usual, just in a different place. Things get more interesting when objects span line breaks. Simple classes like :obj:`.Path` and :obj:`.Text` simply break across the line (clipping at the line edges), but :ref:`other classes can provide variable rendering behavior <advanced rendering>` as an object appears in different places relative to flowable breaks.

Break Opportunities
-------------------

By default, flowable lines run as far as they can within the live page area and break at page margins. Flowables can also be made to respect break opportunities by proactively breaking when one is encountered within its :obj:`break_threshold <.Flowable.break_threshold>`. When calculating its layout, ``Flowable`` finds all descendents which subclass :obj:`.BreakOpportunity`; it then checks at every line break whether any opportunity is placed between the page margin and ``break_threshold`` to the left of it. If such opportunities exist, it will break at the last one encountered.

.. rendered-example::

   from neoscore.core.break_opportunity import BreakOpportunity

   class BreakHintText(Text, BreakOpportunity):
       pass

   flow = Flowable(ORIGIN, None, Mm(500), Mm(15), break_threshold=Mm(50))
   paper = neoscore.document.pages[0].paper
   # Outline the flowable for visualization
   Path.rect(ORIGIN, flow, Mm(500), Mm(15), brush=Brush.no_brush())
   # And draw a line over the break threshold
   Path.straight_line((paper.live_width - Mm(50), ZERO), None, (ZERO, Mm(75)),
       pen=Pen("#ff0000", pattern=PenPattern.DASH))
   BreakHintText((Mm(100), Mm(8)), flow, "opp 1")
   BreakHintText((Mm(200), Mm(8)), flow, "opp 2")
   BreakHintText((Mm(300), Mm(8)), flow, "opp 3")
   BreakHintText((Mm(430), Mm(6)), flow, "opp 4")
   BreakHintText((Mm(440), Mm(12)), flow, "opp 5")

:obj:`.Flowable.break_threshold` is zero by default, meaning break opportunities are always ignored. You can also set it to some value larger than the live page width to make it break at every opportunity.

Dynamic margins
---------------

Flowables can also have dynamically calculated left margins. This is useful in situations like western notation staves, where each staff system line has a left fringe with a clef, key signature, etc., and it is not desirable for that fringe to occupy the flowable coordinate space. In situations like this, the flowable can be made to leave a margin on its side where those elements can be laid out. See :obj:`.Flowable.provided_controllers`.
