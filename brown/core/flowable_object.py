from brown.core.flowable_frame import FlowableFrame



class FlowableObject:

    # Init inherited completely from GraphicObject

    @property
    def flowable(self):
        return self._flowable

    @flowable.setter
    def flowable(self, value):
        self._flowable = value

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
