from brown.core.flowable import Flowable
from brown.core.graphic_object import GraphicObject


class FlowableObject(GraphicObject):

    # Init inherited completely from GraphicObject

    @property
    def flowable():
        return self._flowable

    @flowable.setter
    def flowable(value):
        self._flowable = value

    @property
    def offset():
        return self._offset

    @offset.setter
    def offset(value):
        self._offset = value
