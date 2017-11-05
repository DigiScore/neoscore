def _invalidate_cache(object_self, property_name):
    if property_name in object_self._cache_:
        del object_self._cache_[property_name]
        # Recursively invalidate any caches which depend on this property
        setter_id = id(object_self) + hash(property_name)
        if setter_id in cached_property.dependency_map:
            for listener_object, listener_method in \
                    cached_property.dependency_map[setter_id]:
                _invalidate_cache(listener_object, listener_method.__name__)


class cached_property:

    dependency_map = {}
    caching_properties = set()

    def __init__(self, dependencies=None):
        self.dependencies = dependencies if dependencies else []
        self.first_call = True

    def __call__(self, method):

        def wrapper(*args):
            # args[0] is always the `self` of this property setter
            property_id = id(args[0]) + id(method)
            if property_id not in cached_property.caching_properties:
                # Do one-time setup for caching
                # Ensure the cache dict exists in the object
                cached_property.caching_properties.add(property_id)
                if '_cache_' not in args[0].__dict__:
                    args[0].__dict__['_cache_'] = {}
                # Register this property with any given dependencies
                for dep in self.dependencies:
                    if dep.startswith('self'):
                        dep = dep.replace('self', 'args[0]', 1)
                    dep_object_name, dep_name = dep.rsplit('.', 1)
                    dep_object = eval(dep_object_name)
                    if dep_object:
                        dep_id = id(dep_object) + hash(dep_name)
                        if dep_id in cached_property.dependency_map:
                            cached_property.dependency_map[dep_id].append(
                                (args[0], method))
                        else:
                            cached_property.dependency_map[dep_id] = [
                                (args[0], method)]

            if method.__name__ in args[0]._cache_:
                return args[0]._cache_[method.__name__]
            else:
                value = method(*args)
                args[0]._cache_[method.__name__] = value
                return value

        return wrapper


class cache_broadcaster:

    def __call__(self, method):

        def wrapper(*args):
            # args[0] is always the `self` of this property setter
            _invalidate_cache(args[0], method.__name__)
            # If this property is also cached, invalidate it
            if ('_cache_' in args[0].__dict__
                    and method.__name__ in args[0]._cache_):
                del args[0]._cache_[method.__name__]
            return method(*args)

        return wrapper
