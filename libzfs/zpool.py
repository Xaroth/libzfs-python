from . import bindings
from .nvpair import ptr_to_dict
from .handle import LibZFSHandle
from .utils.conversion import boolean_t, _key_getter, _config_getter

from datetime import datetime

pool_state_t = bindings['pool_state_t']
pool_scan_func_t = bindings['pool_scan_func_t']
dsl_scan_state_t = bindings['dsl_scan_state_t']

vdev_state_t = bindings['vdev_state_t']
vdev_aux_t = bindings['vdev_aux_t']

zpool_errata_t = bindings['zpool_errata_t']
zpool_prop_t = bindings['zpool_prop_t']
zprop_type_t = bindings['zprop_type_t']
zpool_status_t = bindings['zpool_status_t']
zprop_source_t = bindings['zprop_source_t']
zio_type_t = bindings['zio_type_t']
ZPOOL_MAXNAMELEN = bindings['ZPOOL_MAXNAMELEN']


class PoolScanStats(dict):
    pass_start = _key_getter('pass_start', 0, datetime.fromtimestamp)
    start_time = _key_getter('start_time', 0, datetime.fromtimestamp)
    func = _key_getter('func', 0, pool_scan_func_t)
    state = _key_getter('state', 0, dsl_scan_state_t)

    @classmethod
    def from_data(cls, data):
        keys = ['func', 'state', 'start_time', 'end_time',
                'to_examine', 'examined',
                'to_process', 'processed', 'errors',
                'pass_examined', 'pass_start']
        if len(data) < len(keys):
            data = data + ([None] * (len(keys) - len(data)))
        return cls(zip(keys, data))

    def __repr__(self):
        base = dict.__repr__(self)
        return "<%s: %s>" % (self.__class__.__name__, base)


class ZPoolProperties(dict):
    _altnames = {}
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


class VDevStats(dict):
    ops = _key_getter('ops', [], dict)
    bytes = _key_getter('bytes', [], dict)

    state = _key_getter('state', 0, vdev_state_t)
    aux = _key_getter('aux', 0, vdev_aux_t)

    @classmethod
    def from_data(cls, data):
        if len(data) < 27:
            extra = [None, ] * (27 - len(data))
            data += extra
        items = zip(
            ['timestamp', 'state', 'aux', 'alloc', 'space', 'dspace', 'rsize', 'esize'],
            data[:8]
        )
        keys = [x.name for x in zio_type_t if x < zio_type_t.ZIO_TYPES]
        items += (
            ('ops', zip(keys, data[8:14])),
            ('bytes', zip(keys, data[14:20])),
        )
        items += zip(
            ['read_errors', 'write_errors', 'checksum_errors', 'self_healed', 'scan_removing',
            'scan_processed', 'fragmentation'],
            data[20:27]
        )
        return cls(items)

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(other)
        items = [
            (key, self[key] - other[key]) for key in self.keys() if key in other and key not in ['ops', 'bytes', 'fragmentation']
        ]
        for key in ['ops', 'bytes']:
            s, o = getattr(self, key), getattr(other, key)
            new_data = [(x, s[x.name] - o[x.name]) for x in zio_type_t if x < zio_type_t.ZIO_TYPES]
            items.append((key, new_data))
        fragmentation = self['fragmentation']
        items.append(('fragmentation', (fragmentation - other['fragmentation']) if fragmentation is not None else None))
        return self.__class__(items)

    def __repr__(self):
        base = dict.__repr__(self)
        return "<%s: %s>" % (self.__class__.__name__, base)


class VDevItem(dict):
    id = _config_getter('ZPOOL_CONFIG_ID')
    guid = _config_getter('ZPOOL_CONFIG_GUID')
    type = _config_getter('ZPOOL_CONFIG_TYPE')
    create_txg = _config_getter('ZPOOL_CONFIG_CREATE_TXG', -1)
    children = _config_getter('ZPOOL_CONFIG_CHILDREN', [], lambda children: [VDevChild(child) for child in children])
    vdev_stats = _config_getter('ZPOOL_CONFIG_VDEV_STATS', [], VDevStats.from_data)
    scan_stats = _config_getter('ZPOOL_CONFIG_SCAN_STATS', [], PoolScanStats.from_data)

    def __repr__(self):
        base = dict.__repr__(self)
        return "<%s: %s (%s): %s>" % (self.__class__.__name__, self.type, self.guid, base)


class VDevChild(VDevItem):
    ashift = _config_getter('ZPOOL_CONFIG_ASHIFT', -1)
    asize = _config_getter('ZPOOL_CONFIG_ASIZE', -1)
    is_log = _config_getter('ZPOOL_CONFIG_IS_LOG', 0, bool)
    path = _config_getter('ZPOOL_CONFIG_PATH', None)
    nparity = _config_getter('ZPOOL_CONFIG_NPARITY', None)


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
            bindings.libzfs.zpool_close(self._hdl)

    @property
    def hdl(self):
        return self._hdl

    @property
    def name(self):
        if self._name is None:
            self._name = bindings.ffi.string(bindings.libzfs.zpool_get_name(self.hdl))
        return self._name

    @property
    def state(self):
        if self._state is None:
            state = bindings.libzfs.zpool_get_state(self.hdl)
            self._state = pool_state_t(state)
        return self._state

    def _get_status(self):
        if self._status is not None:
            return
        msgid = bindings.ffi.new('char **')
        errata = bindings.ffi.new('zpool_errata_t *')

        reason = bindings.libzfs.zpool_get_status(self.hdl, msgid, errata)

        self._status = zpool_status_t(reason)
        if msgid[0] == bindings.ffi.NULL:
            self._status_extra = ''
        else:
            self._status_extra = bindings.ffi.string(msgid[0])
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
            if bindings.libzfs.zpool_props_refresh(self.hdl) != 0:
                raise Exception("Unable to refresh our zpool properties")
        self._properties = ZPoolProperties()
        self._propertysources = ZPoolPropSources()
        for prop in zpool_prop_t:
            if prop >= zpool_prop_t.ZPOOL_NUM_PROPS:
                continue
            sourceholder = bindings.ffi.new('zprop_source_t *')
            ptype = zprop_type_t(bindings.libzfs.zpool_prop_get_type(int(prop)))
            if ptype == zprop_type_t.PROP_TYPE_NUMBER:
                value = bindings.libzfs.zpool_get_prop_int(self.hdl, int(prop), sourceholder)
            elif ptype == zprop_type_t.PROP_TYPE_INDEX:
                value = bindings.libzfs.zpool_get_prop_int(self.hdl, int(prop), sourceholder)
                valuestr = bindings.ffi.new('char **')
                if bindings.libzfs.zpool_prop_index_to_string(int(prop), value, valuestr) != 0:
                    value = None
                else:
                    value = bindings.ffi.string(valuestr[0])
            else:
                holder = bindings.ffi.new('char [%s]' % ZPOOL_MAXNAMELEN)
                if bindings.libzfs.zpool_get_prop_literal(self.hdl, int(prop), holder, ZPOOL_MAXNAMELEN,
                                                 sourceholder, boolean_t(True)) != 0:
                    value = None
                else:
                    value = bindings.ffi.string(holder)
            if prop not in ZPoolProperties._altnames:
                ZPoolProperties._altnames[prop] = bindings.ffi.string(bindings.libzfs.zpool_prop_to_name(int(prop)))
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
            config = bindings.libzfs.zpool_get_config(self.hdl, bindings.ffi.NULL)
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
                old_config = bindings.libzfs.zpool_get_old_config(self.hdl)
                self._old_config = ZPoolConfig(ptr_to_dict(old_config, free=False))
        return self._old_config

    @LibZFSHandle.requires_refcount
    def refresh_stats(self):
        missing = bindings.ffi.new("boolean_t *")
        success = bindings.libzfs.zpool_refresh_stats(self.hdl, missing) == 0

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

        @bindings.ffi.callback('zpool_iter_f')
        def _callback(handle, arg=None):
            zpool = ZPool(handle)
            pools.append(zpool)
            return 0

        with LibZFSHandle() as hdl:
            bindings.libzfs.zpool_iter(hdl, _callback, bindings.ffi.NULL)

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
