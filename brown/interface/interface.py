from abc import ABC


class Interface(ABC):
    """An interface between a brown object and a PyQt one.
    
    All `brown.interface` classes should subclass this.
    """

    def __init__(self, brown_object):
        """
        Args:
            brown_object: The brown object this interface belongs to 
        """
        self._brown_object = brown_object

    @property
    def brown_object(self):
        return self._brown_object
