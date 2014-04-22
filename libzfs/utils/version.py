import os
from .._version import __latest_libzfs_version__


def detect_libzfs_version():
    return os.environ.get('LIBZFS_VERSION', __latest_libzfs_version__)
