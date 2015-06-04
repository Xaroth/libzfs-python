from .. import bindings

DEFAULT = object()


def _generic_cast(ffi_type, default_value=None):
    def _inner(value=DEFAULT):
        if value is DEFAULT:
            value = default_value
        return bindings.ffi.cast(ffi_type, value)
    _inner.__name__ = ffi_type
    return _inner

boolean_t = _generic_cast('boolean_t', False)


def _config_getter(name, default=None, transform=None):
    key = bindings[name]
    return _key_getter(key, default=default, transform=transform, name=name)


def _key_getter(key, default=None, transform=None, name=None):
    name = name or key

    def _getter(self):
        if transform:
            value = getattr(self, '_%s' % name, None)
            if value is not None:
                return value
        value = self.get(key, default)
        if transform:
            value = transform(value)
            setattr(self, '_%s' % name, value)
        return value
    _getter.__name__ = name
    return property(_getter)
