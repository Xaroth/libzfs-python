from .bindings import manager
import functools

c_libzfs = manager.libzfs
ffi_libzfs = manager.libzfs_ffi


class NoHandleException(Exception):
    def __init__(self):
        super(NoHandleException, self).__init__("There are no open libzfs handles")


class LibZFSHandle(object):
    """
    Wrapper class around libzfs_handle_t
    """

    _global_ptr = None
    _count = 0

    @classmethod
    def _add_ref(cls):
        cls._count += 1
        if cls._global_ptr is None:
            cls._global_ptr = c_libzfs.libzfs_init()
        return cls._global_ptr

    @classmethod
    def _del_ref(cls):
        cls._count -= 1
        if cls._count < 1 and cls._global_ptr is not None:
            cls._count = 0
            c_libzfs.libzfs_fini(cls._global_ptr)
            cls._global_ptr = None

    def __enter__(self):
        return LibZFSHandle._add_ref()

    def __exit__(self, exc_type = None, exc_val = None, exc_tb = None):
        LibZFSHandle._del_ref()

    @classmethod
    def requires_refcount(cls, func):
        @functools.wraps(func)
        def requires_active_handle(*args, **kwargs):
            if cls.refcount() == 0:
                raise NoHandleException()  # You probably want to encase your code in a 'with LibZFSHandle():' block...
            return func(*args, **kwargs)
        return requires_active_handle

    @classmethod
    def auto(cls, func):
        @functools.wraps(func)
        def auto_claim_handle(*args, **kwargs):
            with cls():
                return func(*args, **kwargs)
        return auto_claim_handle

    @classmethod
    def refcount(cls):
        return cls._count

    @classmethod
    def init(cls):
        return LibZFSHandle._add_ref()

    @classmethod
    def fini(cls):
        LibZFSHandle._del_ref()
