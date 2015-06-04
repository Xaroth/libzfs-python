import functools
import atexit


class NoHandleException(Exception):
    def __init__(self):
        super(NoHandleException, self).__init__("There are no open libzfs handles")


class LibZFSHandle(object):
    """
    Wrapper class around libzfs_handle_t.

    You can use ``LibZFSHandle`` as a context manager, or using the class methods :py:func:`LibZFSHandle.init`
    and :py:func:`LibZFSHandle.fini`.

    Furthermore, the decorator functions :py:func:`LibZFSHandle.requires_refcount` and :py:func:`LibZFSHandle.auto`
    provide easy decorators to ensure (or enforce) a valid libzfs handle has been created (and will not be reclaimed
    until a certain section has been completed.)
    """

    _global_ptr = None
    _count = 0

    @classmethod
    def _add_ref(cls):
        from . import bindings
        cls._count += 1
        if cls._global_ptr is None:
            cls._global_ptr = bindings.libzfs.libzfs_init()
        return cls._global_ptr

    @classmethod
    def _del_ref(cls):
        from . import bindings
        cls._count -= 1
        if cls._count < 1 and cls._global_ptr is not None:
            cls._count = 0
            bindings.libzfs.libzfs_fini(cls._global_ptr)
            cls._global_ptr = None

    def __enter__(self):
        return LibZFSHandle._add_ref()

    def __exit__(self, exc_type = None, exc_val = None, exc_tb = None):
        LibZFSHandle._del_ref()

    @classmethod
    def requires_refcount(cls, func):
        """
        The ``requires_refcount`` decorator adds a check prior to call ``func`` to verify
        that there is an active handle. if there is no such handle, a ``NoHandleException`` exception is thrown.
        """
        @functools.wraps(func)
        def requires_active_handle(*args, **kwargs):
            if cls.refcount() == 0:
                raise NoHandleException()  # You probably want to encase your code in a 'with LibZFSHandle():' block...
            return func(*args, **kwargs)
        return requires_active_handle

    @classmethod
    def auto(cls, func):
        """
        The ``auto`` decorator wraps ``func`` in a context manager so that a handle is obtained.

        .. note::
           Please note, that most functions require the handle to continue being alive for future calls to data
           retrieved from the function. In such cases, it's advisable to use the `requires_refcount` decorator, and
           force the program using the library with obtaining a handle (and keeping it active.)
        """
        @functools.wraps(func)
        def auto_claim_handle(*args, **kwargs):
            with cls():
                return func(*args, **kwargs)
        return auto_claim_handle

    @classmethod
    def refcount(cls):
        """
        This function returns the amount of active references for the current global libzfs handle.

        .. note::
           If this function returns 0, no current handle is obtained
        """
        return cls._count

    @classmethod
    def init(cls):
        """
        Requests the current global libzfs handle (or creates one if no handle is active)

        .. note::
           This function increases the refcount by one as such it is needed that :py:func:`LibZFSHandle.fini` is
           called when the process is completed to reduce the refcount, and allow for cleanup.
        """
        return LibZFSHandle._add_ref()

    @classmethod
    def fini(cls):
        """
        This function reduces the refcount by one, and performs cleanup when no more references are active.
        """
        LibZFSHandle._del_ref()


def exit_handler():
    if LibZFSHandle._count:
        LibZFSHandle._count = 0
        LibZFSHandle.fini()

atexit.register(exit_handler)
