from brown.core.flowable import Flowable
from brown.core.flowable_object import FlowableObject

from brown.utils import units

from brown.models.clef import Clef
from brown.models.position import Position


class Staff(FlowableObject):
    def __init__(flowable, offset=None, contents=None):
        '''
        Args:
            flowable (Flowable): The parent flowable
            offset (Position): The offset position of the staff relative
                to the parent flowable
            contents (list): An optional list of initial contents for the staff
        '''
        self.flowable = flowable
        self.offset = offset
        self.offset = offset

    @property
    def contents():
        return self._contents

    @contents.setter
    def contents(value):
        if value is None:
            self._contents = []
        else:
            self._contents = value
