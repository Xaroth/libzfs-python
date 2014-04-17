from enum import IntEnum
from .bindings import libnvpair, libnvpair_ffi

from ..general import boolean_t

from libzfs.utils import six


LOOKUP_DEFAULT = object()


class NVListFlags(IntEnum):
    UNIQUE_NAME = 1
    UNIQUE_NAME_TYPE = 2


class NVList(object):
    def __init__(self, flags=NVListFlags.UNIQUE_NAME, handle=None, alloc=True, free=True):
        self._flags = flags
        self._handle = handle
        self._alloc = alloc
        self._free = free

    def alloc(self):
        if self._handle is None:
            self._handle = libnvpair_ffi.new('nvlist_t **')
        if self._alloc:
            return libnvpair.nvlist_alloc(self._handle, int(self._flags), 0)

    __enter__ = alloc

    def free(self, exc_type, exc_val, exc_tb):
        if self._handle and self._free:
            libnvpair.nvlist_free(self.ptr)
            self._handle = None

    __exit__ = free

    @property
    def ptr(self):
        if self._handle:
            return self._handle[0]
        return None

    @property
    def handle(self):
        return self._handle

    @classmethod
    def from_nvlist_ptr(cls, ptr):
        nvlist = libnvpair_ffi.new('nvlist_t **')
        nvlist[0] = ptr
        return cls.from_nvlist_handle(nvlist)  # We're already allocated

    @classmethod
    def from_nvlist_handle(cls, hdl):
        return cls(handle=hdl, alloc=False)

    def update(self, arg=None, **kwargs):
        if arg:
            if hasattr(arg, 'keys'):
                for k in arg:
                    self.add(k, arg[k])
            else:
                for k, v in arg:
                    self.add(k, v)
        for k, v in kwargs.items():
            self.add(k, v)

    def add(self, key, value):
        k, v = key, value
        if isinstance(v, (int, long)):
            method = libnvpair.nvlist_add_uint64
        elif isinstance(v, six.binary_type):
            method = libnvpair.nvlist_add_string
        elif isinstance(v, bool):
            method = libnvpair.nvlist_add_boolean_value
            v = boolean_t(v)
        else:
            raise Exception("Unknown type for key '%s': '%r'" % (k, v))
        return not bool(method(self.ptr, k, v))

    def lookup(self, key, type, default=LOOKUP_DEFAULT):
        k, t = key, type
        if t in (int, long):
            holder = libnvpair_ffi.new('uint64_t *')
            method = libnvpair.nvlist_lookup_uint64
            if t == int:
                convert = lambda x: int(x[0])
            else:
                convert = lambda x: long(x[0])
        elif t == six.binary_type:
            holder = libnvpair_ffi.new('char **')
            method = libnvpair.nvlist_lookup_string
            convert = lambda x: libnvpair_ffi.string(x[0])
        elif t == bool:
            holder = libnvpair_ffi.new('boolean_t *')
            method = libnvpair.nvlist_lookup_boolean_value
            convert = lambda x: bool(x[0])
        elif t == dict:
            holder = libnvpair_ffi.new('nvlist_t **')
            method = libnvpair.nvlist_lookup_nvlist
            convert = lambda x: NVList.from_nvlist_handle(x)
        else:
            raise Exception("Unknown type for key '%s': '%r'" % (k, t))
        val = method(self.ptr, key, holder)
        if not bool(val):
            return convert(holder)
        elif default is not LOOKUP_DEFAULT:
            return default

    def dump(self):
        return libnvpair.dump_nvlist(self.ptr, 0)
