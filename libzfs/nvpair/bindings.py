from libzfs.bindings import manager
from libzfs.bindings.enums import data_type

c_libnvpair = manager.libnvpair
ffi_libnvpair = manager.libnvpair_ffi

__all__ = [
    'data_type',
    'c_libnvpair',
    'ffi_libnvpair',
]
