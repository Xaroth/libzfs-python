from libzfs.bindings import manager
from libzfs.bindings.enums import DataType

c_libnvpair = manager.libnvpair
ffi_libnvpair = manager.libnvpair_ffi

__all__ = [
    'DataType',
    'c_libnvpair',
    'ffi_libnvpair',
]
