from .libnvpair import (TYPEDEFS as TD_NVPAIR,
                        FUNCTIONS as FN_NVPAIR,
                        INCLUDES as INC_NVPAIR,
                        GENERATE as GEN_NVPAIR)
from .general import   (TYPEDEFS as TD_GENERAL,
                        FUNCTIONS as FN_GENERAL,
                        INCLUDES as INC_GENERAL,
                        GENERATE as GEN_GENERAL)

TYPEDEFS = {
    'general':      TD_GENERAL,
    'libnvpair':    TD_NVPAIR,
}

FUNCTIONS = {
    'general':      FN_GENERAL,
    'libnvpair':    FN_NVPAIR,
}

INCLUDES = {
    'general':      INC_GENERAL,
    'libnvpair':    INC_NVPAIR,
}

GENERATE = {
    'general':      GEN_GENERAL,
    'libnvpair':    GEN_NVPAIR,
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
]
