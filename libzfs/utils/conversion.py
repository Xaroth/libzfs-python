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
