class BreakOpportunity:
    """A :obj:`.PositionedObject` mixin which indicates a break can be performed here.

    Some notational constructs are well suited to be placed at line
    or page breaks, for example bar lines or grand pauses. Such classes
    should subclass this mixin so the flowable container can know this.

    This mixin is only useful when used inside a :obj:`.Flowable`.
    """

    # Type sentinel for faster type lookups
    _neoscore_break_opportunity_type_marker = True
