from . import bindings
from .nvpair import ptr_to_dict
from .handle import LibZFSHandle
from .utils.conversion import boolean_t

from datetime import datetime

libzfs = bindings.libzfs
ffi = bindings.ffi

pool_state_t = bindings['pool_state_t']
zpool_errata_t = bindings['zpool_errata_t']
zpool_prop_t = bindings['zpool_prop_t']
zprop_type_t = bindings['zprop_type_t']
zpool_status_t = bindings['zpool_status_t']
zprop_source_t = bindings['zprop_source_t']
ZPOOL_MAXNAMELEN = bindings['ZPOOL_MAXNAMELEN']


def _config_getter(key, default=None, transform=None):
    def _getter(self):
        if transform:
            value = getattr(self, '_%s' % key, None)
            if value is not None:
                return value
        value = self.get(bindings[key], default)
        if transform:
            value = transform(value)
            setattr(self, '_%s' % key, value)
        return value
    _getter.__name__ = key
    return property(_getter)


class ZPoolProperties(dict):
    name = _config_getter('ZPOOL_PROP_NAME')
    size = _config_getter('ZPOOL_PROP_SIZE', -1)
    capacity = _config_getter('ZPOOL_PROP_CAPACITY', -1)
    allocated = _config_getter('ZPOOL_PROP_ALLOCATED', -1)
    free = _config_getter('ZPOOL_PROP_FREE', -1)
    version = _config_getter('ZPOOL_PROP_VERSION', -1)
    fragmentation = _config_getter('ZPOOL_PROP_FRAGMENTATION', 0)

    def __repr__(self):
        base = dict.__repr__(self)
        return "<%s: %s: %s>" % (self.__class__.__name__, self.name, base)


class ZPoolPropSources(dict):
    def __repr__(self):
        base = dict.__repr__(self)
        return "<%s: %s>" % (self.__class__.__name__, base)


class VDevItem(dict):
    id = _config_getter('ZPOOL_CONFIG_ID')
    guid = _config_getter('ZPOOL_CONFIG_GUID')
    type = _config_getter('ZPOOL_CONFIG_TYPE')
    create_txg = _config_getter('ZPOOL_CONFIG_CREATE_TXG', -1)
    children = _config_getter('ZPOOL_CONFIG_CHILDREN', [], lambda children: [VDevChild(child) for child in children])

    def __repr__(self):
        base = dict.__repr__(self)
        return "<%s: %s (%s): %s>" % (self.__class__.__name__, self.type, self.guid, base)


class VDevChild(VDevItem):
    ashift = _config_getter('ZPOOL_CONFIG_ASHIFT', -1)
    asize = _config_getter('ZPOOL_CONFIG_ASIZE', -1)
    is_log = _config_getter('ZPOOL_CONFIG_IS_LOG', 0, bool)


class VDevTree(VDevItem):
    pass


class ZPoolConfig(dict):
    name = _config_getter('ZPOOL_CONFIG_POOL_NAME')
    guid = _config_getter('ZPOOL_CONFIG_POOL_GUID')
    hostid = _config_getter('ZPOOL_CONFIG_HOSTID')
    hostname = _config_getter('ZPOOL_CONFIG_HOSTNAME')
    version = _config_getter('ZPOOL_CONFIG_VERSION', -1)
    initial_load_time = _config_getter('ZPOOL_CONFIG_LOADED_TIME', 0, lambda x: datetime.fromtimestamp(x[0]))

    error_count = _config_getter('ZPOOL_CONFIG_ERRCOUNT', 0)
    feature_stats = _config_getter('ZPOOL_CONFIG_FEATURE_STATS', {})
    features_for_read = _config_getter('ZPOOL_CONFIG_FEATURES_FOR_READ', {})

    vdev_tree = _config_getter('ZPOOL_CONFIG_VDEV_TREE', {}, VDevTree)
    current_txg = _config_getter('ZPOOL_CONFIG_POOL_TXG', -1)

    def __repr__(self):
        base = dict.__repr__(self)
        return "<ZPoolConfig: %s: %s>" % (self.name, base)


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

    def __init__(self, hdl):
        self._hdl = hdl

    def __del__(self):
        if hasattr(self, '_hdl'):
            libzfs.zpool_close(self._hdl)

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
        self._properties = ZPoolProperties()
        self._propertysources = ZPoolPropSources()
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
            self._config = ZPoolConfig(ptr_to_dict(config, free=False))
        return self._config

    @property
    def old_config(self):
        if self._old_config is None:
            if self._refreshed:
                # Judging by zfs/cmd/zpool/zpool_main.c, we should ignore the 'old config'
                #  the first time we refresh the iostats.
                # The internals (zfs/lib/libzfs/libzfs_config.c) should probably clarify more
                #  on why.. for now we'll mimic what we see.
                old_config = libzfs.zpool_get_old_config(self.hdl)
            self._old_config = ZPoolConfig(ptr_to_dict(old_config, free=False))
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
            pools = [pool for pool in pools if pool.config.name == name]
        if guid:
            pools = [pool for pool in pools if pool.config.guid == guid]

        if len(pools) == 1:
            return pools[0]
        raise KeyError("Could not find %s matching query" % cls.__name__)
