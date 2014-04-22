from .general import (TYPEDEFS as TD_GENERAL,
                      FUNCTIONS as FN_GENERAL,
                      INCLUDES as INC_GENERAL,
                      GENERATE as GEN_GENERAL,
                      VERSION_SPECIFIC as VERSION_GENERAL)
from .libnvpair import (TYPEDEFS as TD_NVPAIR,
                        FUNCTIONS as FN_NVPAIR,
                        INCLUDES as INC_NVPAIR,
                        GENERATE as GEN_NVPAIR,
                        VERSION_SPECIFIC as VERSION_NVPAIR)
from .libzfs import (TYPEDEFS as TD_ZFS,
                     FUNCTIONS as FN_ZFS,
                     INCLUDES as INC_ZFS,
                     GENERATE as GEN_ZFS,
                     VERSION_SPECIFIC as VERSION_ZFS)

from ... import libzfs_version

TYPEDEFS = {
    'general':      TD_GENERAL,
    'libnvpair':    TD_NVPAIR,
    'libzfs':       TD_ZFS,
}

FUNCTIONS = {
    'general':      FN_GENERAL,
    'libnvpair':    FN_NVPAIR,
    'libzfs':       FN_ZFS,
}

INCLUDES = {
    'general':      INC_GENERAL,
    'libnvpair':    INC_NVPAIR,
    'libzfs':       INC_ZFS,
}

GENERATE = {
    'general':      GEN_GENERAL,
    'libnvpair':    GEN_NVPAIR,
    'libzfs':       GEN_ZFS,
}

VERSION_SPECIFIC = {
    'general':      VERSION_GENERAL,
    'libnvpair':    VERSION_NVPAIR,
    'libzfs':       VERSION_ZFS,
}


def verify(ffi):
    return ffi.verify("""
    #include <libzfs.h>
    #include <sys/fs/zfs.h>
    #include <sys/types.h>
    #include <libnvpair.h>
    """,
    define_macros=[
        ('NDEBUG', 1),
        ('HAVE_IOCTL_IN_SYS_IOCTL_H', 1),
    ], include_dirs=[
        '/usr/include/libzfs',
        '/usr/include/libspl',
    ], libraries=[
        'nvpair',
        'zfs',
        'zpool',
    ])


__all__ = [
    'TYPEDEFS',
    'FUNCTIONS',
    'INCLUDES',
    'VERSION_SPECIFIC',
]
