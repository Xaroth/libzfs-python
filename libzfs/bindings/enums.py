import os
try:
    uname = os.uname()[0].lower()
except AttributeError:
    # uname is not available, we're most likely running on a non-unix-like system
    # (aka windows)
    uname = 'unknown'

from .generic.enums import *  # noqa

if 'linux' in uname:
    # Todo: load linux-specific changes
    pass
elif 'freebsd' in uname:
    # Todo: load bsd-specific changes
    pass
elif 'darwin' in uname:
    # Todo: load osx-specific changes
    pass
