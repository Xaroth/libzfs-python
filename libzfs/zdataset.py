from . import bindings
from .handle import LibZFSHandle
from .utils.conversion import boolean_t

libzfs = bindings.libzfs
ffi = bindings.ffi

zfs_type_t = bindings['zfs_type_t']


class ZDataset(object):
    def __init__(self, hdl):
        self._hdl = hdl
        self._type = zfs_type_t(libzfs.zfs_get_type(hdl))
        self._name = ffi.string(libzfs.zfs_get_name(hdl))

    def __del__(self):
        if hasattr(self, '_hdl'):
            libzfs.zfs_close(self._hdl)

    def __repr__(self):
        return "<%s: %s: %r>" % (self.__class__.__name__, self._name, self._type)

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def hdl(self):
        return self._hdl

    @classmethod
    @LibZFSHandle.requires_refcount
    def list(cls):
        datasets = []

        @ffi.callback('zfs_iter_f')
        def _callback(handle, arg=None):
            zpool = ZDataset(handle)
            datasets.append(zpool)
            return 0

        with LibZFSHandle() as hdl:
            libzfs.zfs_iter_root(hdl, _callback, ffi.NULL)

        return datasets

    @classmethod
    @LibZFSHandle.requires_refcount
    def open(cls, name, zfs_type):
        try:
            zfs_type = zfs_type_t(int(zfs_type))
        except ValueError:
            raise ValueError("Unknown zfs_type_t")
        with LibZFSHandle() as hdl:
            zhp = libzfs.zfs_open(hdl, name, zfs_type)

        if zhp == ffi.NULL:
            raise KeyError("Unknown dataset: %s" % name)
        return ZDataset(zhp)

    @LibZFSHandle.requires_refcount
    @LibZFSHandle.auto
    def _iter(self, func, extra=None):
        datasets = []

        @ffi.callback('zfs_iter_f')
        def _callback(handle, arg=None):
            zpool = ZDataset(handle)
            datasets.append(zpool)
            return 0
        args = [_callback, ffi.NULL]
        if extra is not None:
            args.insert(0, extra)
        func(self.hdl, *args)
        return datasets

    def children(self):
        return self._iter(libzfs.zfs_iter_children)

    def child_filesystems(self):
        return self._iter(libzfs.zfs_iter_filesystems)

    def child_snapshots(self):
        return self._iter(libzfs.zfs_iter_snapshots, boolean_t(False))
