from .bindings import manager

c_libzfs = manager.libzfs
ffi_libzfs = manager.libzfs_ffi


class LibZFSHandle(object):
    """
    Wrapper class around libzfs_handle_t
    """

    _global_ptr = None

    def __init__(self):
        self._ptr = None

    def __enter__(self):
        if not self._ptr:
            self._ptr = c_libzfs.libzfs_init()

    def __exit__(self, exc_type = None, exc_val = None, exc_tb = None):
        if self._ptr is not None:
            c_libzfs.libzfs_fini(self._ptr)
            self._ptr = None

    @classmethod
    def init(cls, auto_release = False):
        """
        Initializes a handle with libzfs

        :param auto_release: use cffi's gc function to auto-release the handle (not recommended). Default False.
        :type auto_release: bool.
        """
        if not cls._global_ptr:
            if auto_release:
                def _fini(ptr):
                    if ptr == cls._global_ptr:
                        cls._global_ptr = None
                    c_libzfs.libzfs_fini(ptr)
                cls._global_ptr = ffi_libzfs.gc(c_libzfs.libzfs_init(), _fini)
            else:
                cls._global_ptr = c_libzfs.libzfs_init()

    @classmethod
    def fini(cls):
        """
        Closes the handle with libzfs

        .. note::
           If the handle was created with ``auto_release`` set to True, this should not need to be called.

        .. note::
           There should be no harm to calling this function more than once.
           Once the global handle has been closed, this function does nothing until a new one is opened.
        """
        if cls._global_ptr is not None:
            c_libzfs.libzfs_fini(cls._global_ptr)
            cls._global_ptr = None
