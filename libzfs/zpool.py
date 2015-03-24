from . import bindings
from .nvpair import ptr_to_dict
from .handle import LibZFSHandle
from .utils.conversion import boolean_t

libzfs = bindings.libzfs
ffi = bindings.ffi

pool_state_t = bindings['pool_state_t']
zpool_errata_t = bindings['zpool_errata_t']
zpool_prop_t = bindings['zpool_prop_t']
zprop_type_t = bindings['zprop_type_t']
zpool_status_t = bindings['zpool_status_t']
zprop_source_t = bindings['zprop_source_t']
ZPOOL_MAXNAMELEN = bindings['ZPOOL_MAXNAMELEN']
ZPOOL_CONFIG_POOL_NAME = bindings['ZPOOL_CONFIG_POOL_NAME']
ZPOOL_CONFIG_POOL_GUID = bindings['ZPOOL_CONFIG_POOL_GUID']


class ZPool(object):
    _name = None
    _state = None
    _config = None
    _old_config = None
    _refreshed = False

    _properties = None
    _propertysources = None

    _status = None
    _status_extra = None
    _errata = None

    def __init__(self, handle):
        self._hdl = handle

    @property
    def hdl(self):
        return self._hdl

    @property
    def name(self):
        if self._name is None:
            self._name = ffi.string(libzfs.zpool_get_name(self.hdl))
        return self._name

    @property
    def state(self):
        if self._state is None:
            state = libzfs.zpool_get_state(self.hdl)
            self._state = pool_state_t(state)
        return self._state

    def _get_status(self):
        if self._status is not None:
            return
        msgid = ffi.new('char **')
        errata = ffi.new('zpool_errata_t *')

        reason = libzfs.zpool_get_status(self.hdl, msgid, errata)

        self._status = zpool_status_t(reason)
        if msgid[0] == ffi.NULL:
            self._status_extra = ''
        else:
            self._status_extra = ffi.string(msgid[0])
        self._errata = zpool_errata_t(errata[0])

    @property
    def status_extra(self):
        self._get_status()
        return self._status_extra

    @property
    def status(self):
        self._get_status()
        return self._status

    @property
    def errata(self):
        self._get_status()
        return self._errata

    @LibZFSHandle.requires_refcount
    @LibZFSHandle.auto
    def refresh_properties(self):
        if self._properties is not None:
            if libzfs.zpool_props_refresh(self.hdl) != 0:
                raise Exception("Unable to refresh our zpool properties")
        self._properties = {}
        self._propertysources = {}
        for prop in zpool_prop_t:
            if prop >= zpool_prop_t.ZPOOL_NUM_PROPS:
                continue
            sourceholder = ffi.new('zprop_source_t *')
            ptype = zprop_type_t(libzfs.zpool_prop_get_type(int(prop)))
            if ptype == zprop_type_t.PROP_TYPE_NUMBER:
                value = libzfs.zpool_get_prop_int(self.hdl, int(prop), sourceholder)
            elif ptype == zprop_type_t.PROP_TYPE_INDEX:
                value = libzfs.zpool_get_prop_int(self.hdl, int(prop), sourceholder)
                valuestr = ffi.new('char **')
                if libzfs.zpool_prop_index_to_string(int(prop), value, valuestr) != 0:
                    value = None
                else:
                    value = ffi.string(valuestr[0])
            else:
                holder = ffi.new('char [%s]' % ZPOOL_MAXNAMELEN)
                if libzfs.zpool_get_prop_literal(self.hdl, int(prop), holder, ZPOOL_MAXNAMELEN,
                                                 sourceholder, boolean_t(True)) != 0:
                    value = None
                else:
                    value = ffi.string(holder)
            self._properties[prop] = value
            self._propertysources[prop] = zprop_source_t(sourceholder[0])

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
    def config(self):
        if self._config is None:
            config = libzfs.zpool_get_config(self.hdl, ffi.NULL)
            self._config = ptr_to_dict(config, free=False)
        return self._config

    @property
    def old_config(self):
        if self._refreshed is False:
            # Judging by zfs/cmd/zpool/zpool_main.c, we should ignore the 'old config'
            #  the first time we refresh the iostats.
            # The internals (zfs/lib/libzfs/libzfs_config.c) should probably clarify more
            #  on why.. for now we'll mimic what we see.
            return dict()
        if self._old_config is None:
            old_config = libzfs.zpool_get_old_config(self.hdl)
            self._old_config = ptr_to_dict(old_config, free=False)
        return self._old_config

    @LibZFSHandle.requires_refcount
    def refresh_stats(self):
        missing = ffi.new("boolean_t *")
        success = libzfs.zpool_refresh_stats(self.hdl, missing) == 0

        missing = bool(missing[0])

        success = success and not missing
        if success:
            self._config = None
            self._old_config = None
            self._refreshed = True

        return success

    def __repr__(self):
        return "<ZPool: %s: %s>" % (self.name, self.state.name)

    @classmethod
    @LibZFSHandle.requires_refcount
    def list(cls):
        pools = []

        @ffi.callback('zpool_iter_f')
        def _callback(handle, arg=None):
            zpool = ZPool(handle)
            pools.append(zpool)
            return 0

        with LibZFSHandle() as hdl:
            libzfs.zpool_iter(hdl, _callback, ffi.NULL)

        return pools

    @classmethod
    @LibZFSHandle.requires_refcount
    def get(cls, name=None, guid=None):
        if guid:
            guid = int(guid)

        pools = cls.list()

        if name:
            pools = [pool for pool in pools if pool.config.get(ZPOOL_CONFIG_POOL_NAME) == name]
        if guid:
            pools = [pool for pool in pools if pool.config.get(ZPOOL_CONFIG_POOL_GUID) == guid]

        if len(pools) == 1:
            return pools[0]
        raise KeyError("Could not find %s matching query" % cls.__name__)
