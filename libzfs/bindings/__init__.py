import os
uname = os.uname()[0].lower()

from .generic import *  # noqa

if 'linux' in uname:
    # Todo: load linux-specific changes
    pass
elif 'freebsd' in uname:
    # Todo: load bsd-specific changes
    pass
elif 'darwin' in uname:
    # Todo: load osx-specific changes
    pass
