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


def _get_iterfunc(funcname, extra=False):
    func = getattr(bindings.libzfs, funcname)

    @LibZFSHandle.requires_refcount
    @LibZFSHandle.auto
    def _inner(self):
        datasets = []

        @ffi.callback('zfs_iter_f')
        def _cb(hdl, arg=None):
            ds = ZDataset(hdl)
            datasets.append(ds)
            return 0

        args = [_cb, bindings.ffi.NULL]
        if extra:
            args.insert(0, boolean_t(False))

        func(self.hdl, *args)
        return datasets

    return property(_inner)


class ZDatasetProperties(dict):
    _altnames = {}
    pass


class ZDataset(object):
    _properties = None
    _propertysources = None
    _propertynames = None

    children = _get_iterfunc('zfs_iter_children')
    child_filesystems = _get_iterfunc('zfs_iter_filesystems')
    child_snapshots = _get_iterfunc('zfs_iter_snapshots', True)

    def reset_children(self):
        self._zfs_iter_children = None
        self._zfs_iter_filesystems = None
        self._zfs_iter_snapshots = None

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
    def guid(self):
        return self.properties.get(zfs_prop_t.ZFS_PROP_GUID)

    @property
    def hdl(self):
        return self._hdl

    @LibZFSHandle.requires_refcount
    @LibZFSHandle.auto
    def refresh_properties(self):
        self._properties = ZDatasetProperties()
        self._propertysources = {}

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

            if prop not in ZDatasetProperties._altnames:
                ZDatasetProperties._altnames[prop] = bindings.ffi.string(bindings.libzfs.zfs_prop_to_name(int(prop)))
            self._propertysources[prop] = zprop_source_t(sourceholder[0])
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
    def get(cls, name=None, guid=None):
        if guid:
            guid = int(guid)

        datasets = cls.list()

        if name:
            datasets = [dataset for dataset in datasets if dataset.name == name]
        if guid:
            datasets = [dataset for dataset in datasets if dataset.guid == guid]

        if len(datasets) == 1:
            return datasets[0]
        raise KeyError("Could not find %s matching query" % cls.__name__)

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
