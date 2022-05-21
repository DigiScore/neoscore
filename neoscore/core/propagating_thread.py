from threading import Thread


# Courtesy of https://stackoverflow.com/a/31614591/5615927
class PropagatingThread(Thread):
    """A ``Thread`` which propagates uncaught exceptions."""

    def run(self):
        self.exc = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            self.exc = e

    def join(self, timeout=None):
        super(PropagatingThread, self).join(timeout)
        if self.exc:
            raise self.exc
        return self.ret
