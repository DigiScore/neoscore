from brown.core.time_signature import TimeSignature
from brown.managed.container import Container


class Measure(Container):
    """A metered time measure."""

    def __init__(self, duration, *args, **kwargs):
        self._duration = duration
        super().__init__(*args, **kwargs)

    @property
    def duration(self):
        """Duration: The total length of the Measure"""
        return self._duration

    @property
    def has_time_signature_change(self):
        """Whether or not a time signature change exists in this measure.

        TODO: Optimize
        """
        return any(isinstance(item, TimeSignature) for item in self)
