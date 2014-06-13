from ..bindings import manager
general_ffi = manager.general_ffi


def boolean_t(value=None):
    return general_ffi.cast('boolean_t', value)
