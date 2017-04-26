class Container(list):
    """A logical container of musical objects in sequential order.

    A container is essentially a list of musical objects
    (typically StaffObjects) which can be manipulated and used
    to logically organize structured musical information.

    The most obvious use case for this is in the context of a Staff,
    where it is highly desirable to be able to create objects like
    Chordrests and spanners by specifying their musical properties
    alone, allowing the Staff (or whatever layout system) to decide
    exactly where and how these objects should be displayed.
    """

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, super().__repr__())
