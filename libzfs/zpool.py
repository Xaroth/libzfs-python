from .bindings import manager, enums
from .handle import LibZFSHandle

from .nvpair import NVList

c_libzfs = manager.libzfs
ffi_libzfs = manager.libzfs_ffi


class ZPool(object):
    _name = None
    _state = None
    _config = None

    def __init__(self, handle):
        self._handle = handle

    @property
    def name(self):
        if self._name is None:
            self._name = ffi_libzfs.string(c_libzfs.zpool_get_name(self._handle))
        return self._name

    @property
    def state(self):
        if self._state is None:
            state = c_libzfs.zpool_get_state(self._handle)
            self._state = enums.pool_state(state)
        return self._state

    @property
    def config(self):
        if self._config is None:
            config = c_libzfs.zpool_get_config(self._handle, ffi_libzfs.new_handle(None))
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
