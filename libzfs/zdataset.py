from . import bindings
from .handle import LibZFSHandle
from .utils.conversion import boolean_t

libzfs = bindings.libzfs
ffi = bindings.ffi

zfs_type_t = bindings['zfs_type_t']
zprop_type_t = bindings['zprop_type_t']
zfs_prop_t = bindings['zfs_prop_t']
zprop_source_t = bindings['zprop_source_t']
ZFS_MAXNAMELEN = bindings['ZFS_MAXNAMELEN']


class ZDataset(object):
    _properties = None
    _propertysources = None
    _propertynames = None

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

    @LibZFSHandle.requires_refcount
    @LibZFSHandle.auto
    def refresh_properties(self):
        self._properties = {}
        self._propertysources = {}
        self._propertynames = {}

        for prop in zfs_prop_t:
            if prop >= zfs_prop_t.ZFS_NUM_PROPS:
                continue
            if not bool(libzfs.zfs_prop_valid_for_type(int(prop), int(self._type), boolean_t(False))):
                continue

            sourceholder = ffi.new('zprop_source_t *')
            statbuf = ffi.new('char [%s]' % ZFS_MAXNAMELEN)
            ptype = zprop_type_t(libzfs.zfs_prop_get_type(int(prop)))
            value = None

            if ptype == zprop_type_t.PROP_TYPE_NUMBER:
                holder = ffi.new("uint64_t *")
                res = libzfs.zfs_prop_get_numeric(self.hdl, int(prop), holder, sourceholder, statbuf, ZFS_MAXNAMELEN)
                if res == 0:
                    value = int(holder[0])
            else:
                holder = ffi.new("char [%s]" % ZFS_MAXNAMELEN)
                res = libzfs.zfs_prop_get(self.hdl, int(prop), holder, ZFS_MAXNAMELEN, sourceholder, statbuf,
                                          ZFS_MAXNAMELEN, boolean_t(True))
                if res == 0:
                    value = ffi.string(holder)

            name = ffi.string(libzfs.zfs_prop_to_name(int(prop)))
            self._propertysources[prop] = zprop_source_t(sourceholder[0])
            self._propertynames[prop] = name
            self._properties[prop] = value

    @property
    def properties(self):
        if self._properties is None:
            self.refresh_properties()
        return self._properties

    @property
    def propertysources(self):
        if self._propertysources is None:
            self.refresh_properties()
        return self._propertysources

    @property
    def propertynames(self):
        if self._propertynames is None:
            self.refresh_properties()
        return self._propertynames

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
