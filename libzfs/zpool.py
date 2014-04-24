from .bindings import manager, enums
from .handle import LibZFSHandle
from .general import boolean_t

from .nvpair import NVList

c_libzfs = manager.libzfs
ffi_libzfs = manager.libzfs_ffi


class ZPoolProperties(object):
    def __init__(self, pool):
        self._pool = pool

    @LibZFSHandle.requires_refcount
    def items(self):
        with LibZFSHandle():
            #
            # We add another claim to the handle, to ensure that it remains open during the length of this generator
            for i in range(enums.zpool_prop.NUM_PROPS):
                value, source = self._get_prop(i)
                yield enums.zpool_prop(i), value

    @LibZFSHandle.requires_refcount
    def sources(self):
        with LibZFSHandle():
            #
            # We add another claim to the handle, to ensure that it remains open during the length of this generator
            for i in range(enums.zpool_prop.NUM_PROPS):
                value, source = self._get_prop(i)
                yield enums.zpool_prop(i), source

    @LibZFSHandle.requires_refcount
    def _get_prop(self, key, literal = True):
        holder = ffi_libzfs.new('char [%s]' % enums.ZPOOL_MAXNAMELEN)
        sourceholder = ffi_libzfs.new('zprop_source_t *')
        literal = boolean_t(literal)

        val = c_libzfs.zpool_get_prop_literal(self._pool._handle, int(key), holder,
            enums.ZPOOL_MAXNAMELEN, sourceholder, literal)
        if not bool(val):
            value = ffi_libzfs.string(holder)
            source = enums.zprop_source(sourceholder[0])
            return value, source
        return None, None

    def __getitem__(self, key):
        key = enums.zpool_prop(key)
        value, source = self._get_prop(key)
        if value is None:
            return KeyError(key)
        return value

    def __setitem__(self, key, value):
        # TODO: writing properties
        pass


class ZPool(object):
    _name = None
    _state = None
    _config = None

    def __init__(self, handle):
        self._handle = handle
        self.properties = ZPoolProperties(self)

    @property
    def hdl(self):
        return self._handle

    @property
    def name(self):
        if self._name is None:
            self._name = ffi_libzfs.string(c_libzfs.zpool_get_name(self.hdl))
        return self._name

    @property
    def state(self):
        if self._state is None:
            state = c_libzfs.zpool_get_state(self.hdl)
            self._state = enums.pool_state(state)
        return self._state

    @property
    def config(self):
        if self._config is None:
            config = c_libzfs.zpool_get_config(self.hdl, ffi_libzfs.new_handle(None))
            config_list = NVList.from_nvlist_ptr(config)
            with config_list:
                self._config = config_list.to_dict(skip_unknown = True)
        return self._config

    def __repr__(self):
        return "<ZPool: %s: %s>" % (self.name, self.state.name)

    @classmethod
    def list(cls):
        pools = []

        @ffi_libzfs.callback('zpool_iter_f')
        def _callback(handle, arg=None):
            zpool = ZPool(handle)
            pools.append(zpool)
            return 0

        with LibZFSHandle() as hdl:
            c_libzfs.zpool_iter(hdl, _callback, ffi_libzfs.new_handle(None))

        return pools
