from abc import ABC


class Command(ABC):

    def __init__(self, receiver):
        """
        Args:
            receiver (Any): the object which this command operates on
        """
        self._receiver = receiver

    @property
    def receiver(self):
        """Any: the object which this command operates on.

        Implementing classes will generally place additional type constraints
        on this property.
        """
        return self._receiver

    def execute(self):
        """Execute the command on the receiver"""
        raise NotImplementedError

    def undo(self):
        """Execute the inverse of the command on the receiver.

        It is assumed that the last command executed was `self`.

        This *must* return the document state to how it was before
        the `execute` method was invoked.

        Tests of `undo` methods should include an `execute()` - `undo()`
        equality check.

        Returns: None
        """
        raise NotImplementedError
