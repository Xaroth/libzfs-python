from . import bindings
from .nvpair import NVList
from .handle import LibZFSHandle
from .utils.conversion import boolean_t
from .utils import six

libzfs = bindings.libzfs
ffi = bindings.ffi

pool_state_t = bindings['pool_state_t']
zpool_errata_t = bindings['zpool_errata_t']
zpool_prop_t = bindings['zpool_prop_t']
zpool_status_t = bindings['zpool_status_t']
zprop_source_t = bindings['zprop_source_t']
ZPOOL_MAXNAMELEN = bindings['ZPOOL_MAXNAMELEN']


class ZPoolProperties(object):
    def __init__(self, pool):
        self._pool = pool

    @LibZFSHandle.requires_refcount
    def items(self):
        # We add another claim to the handle, to ensure that it remains open during the length of this generator
        with LibZFSHandle():
            for prop in zpool_prop_t:
                if prop >= zpool_prop_t.ZPOOL_NUM_PROPS:
                    continue
                value, source = self._get_prop(prop)
                yield prop, value

    @LibZFSHandle.requires_refcount
    def sources(self):
        # We add another claim to the handle, to ensure that it remains open during the length of this generator
        with LibZFSHandle():
            for prop in zpool_prop_t:
                if prop >= zpool_prop_t.ZPOOL_NUM_PROPS:
                    continue
                value, source = self._get_prop(prop)
                yield prop, source

    @LibZFSHandle.requires_refcount
    def _get_prop(self, key, literal = True):
        holder = ffi.new('char [%s]' % ZPOOL_MAXNAMELEN)
        sourceholder = ffi.new('zprop_source_t *')
        literal = boolean_t(literal)

        val = libzfs.zpool_get_prop_literal(self._pool._handle, int(key), holder,
                                            ZPOOL_MAXNAMELEN, sourceholder, literal)
        if not bool(val):
            value = ffi.string(holder)
            source = zprop_source_t(sourceholder[0])
            return value, source
        return None, None

    def __getitem__(self, key):
        try:
            key = zpool_prop_t(key)
        except ValueError:
            raise KeyError(key)
        value, source = self._get_prop(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        # TODO: writing properties
        pass


class ZPool(object):
    _name = None
    _state = None
    _config = None
    _old_config = None
    _refreshed = False

    _status = None
    _status_extra = None
    _errata = None

    def __init__(self, handle):
        self._handle = handle
        self.properties = ZPoolProperties(self)

    @property
    def hdl(self):
        return self._handle

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
        if self._status is None:
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

    @property
    def config(self):
        if self._config is None:
            config = libzfs.zpool_get_config(self.hdl, ffi.NULL)
            config_list = NVList.from_nvlist_ptr(config, free=False)
            with config_list:
                self._config = dict(config_list.items(skip_unknown=True))
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
            old_config_list = NVList.from_nvlist_ptr(old_config, free=False)
            with old_config_list:
                self._old_config = dict(old_config_list.items(skip_unknown=True))
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
