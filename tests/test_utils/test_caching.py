import unittest

from brown.utils.caching import cached_property, cache_broadcaster


class CachingClass:

    def __init__(self, number, dependency=None):
        self._number = number
        self.dependency = dependency

    @property
    @cached_property(['self.dependency.number'])
    def number(self):
        if self.dependency:
            return self._number + self.dependency.number
        else:
            return self._number

    @number.setter
    @cache_broadcaster()
    def number(self, value):
        self._number = value


class TestCaching(unittest.TestCase):

    def test_simple_dep(self):
        dep = CachingClass(1000)
        listener = CachingClass(5, dep)
        assert(dep.number == 1000)
        assert(listener.number == 1005)
        listener.number = 10
        assert (dep.number == 1000)
        assert (listener.number == 1010)
        dep.number = 0
        assert(dep.number == 0)
        assert(listener.number == 10)

    def test_chained_dep(self):
        dep = CachingClass(1000)
        listener = CachingClass(5, dep)
        chained_listener = CachingClass(1000, listener)
        assert(chained_listener.number == 2005)
        dep.number = 0
        assert(chained_listener.number == 1005)
