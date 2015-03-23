from . import bindings
from .utils.conversion import boolean_t
from .utils import six

NV_UNIQUE_NAME = bindings['NV_UNIQUE_NAME']
NV_UNIQUE_NAME_TYPE = bindings['NV_UNIQUE_NAME_TYPE']

data_type_t = bindings['data_type_t']


def data_type_t_safe(id):
    try:
        return data_type_t(id)
    except ValueError:
        return None

ffi = bindings.ffi
libzfs = bindings.libzfs

NO_DEFAULT = object()
HOLDER_TYPE = 'uint_t *'


def _split_dict(base, keys_to_split):
    a, b = {}, {}
    for key, value in base.items():
        (b if key in keys_to_split else a)[key] = value
    return a, b


def nvlist_to_dict(nvlist, **kwargs):
    kwargs.setdefault('skip_unknown', True)
    with nvlist:
        return dict(nvlist.items(**kwargs))


def ptr_to_dict(ptr, **kwargs):
    dict_kwargs, nvlist_kwargs = _split_dict(kwargs, ['free', 'alloc', 'flags'])
    nvlist = NVList.from_nvlist_ptr(ptr, **nvlist_kwargs)
    return nvlist_to_dict(nvlist, **dict_kwargs)


def hdl_to_dict(hdl, **kwargs):
    dict_kwargs, nvlist_kwargs = _split_dict(kwargs, ['free', 'alloc', 'flags'])
    nvlist = NVList.from_nvlist_hdl(hdl, **nvlist_kwargs)
    return nvlist_to_dict(nvlist, **dict_kwargs)


class UnknownDataType(Exception):
    pass


class NVPairMixIn(object):
    @classmethod
    def _detect_type(cls, data_type, default=NO_DEFAULT):
        info = NVLIST_HANDLERS.get(data_type)
        if not info and default is NO_DEFAULT:
            raise UnknownDataType("Unknown data type: %r" % data_type)
        elif not info:
            info = default
        return info

    @classmethod
    def _from_python(cls, data_type, data):
        info = cls._detect_type(data_type)
        return info.convert_from_python(data)

    @classmethod
    def _to_python(cls, data_type, data, count=None):
        info = cls._detect_type(data_type)
        return info.convert_to_python(data, count)


class NVList(NVPairMixIn):
    @classmethod
    def from_nvlist_ptr(cls, ptr, **kwargs):
        hdl = ffi.new('nvlist_t **')
        hdl[0] = ptr
        if 'hdl' in kwargs:
            del kwargs['hdl']
        return cls.from_nvlist_hdl(hdl, **kwargs)

    @classmethod
    def from_nvlist_hdl(cls, hdl, **kwargs):
        kwargs['alloc'] = False
        return cls(hdl=hdl, **kwargs)

    def __init__(self, flags=NV_UNIQUE_NAME, hdl=None, alloc=True, free=True):
        self._flags = flags
        self._hdl = hdl
        self._alloc = alloc
        self._alloced = None
        self._free = free

    def alloc(self):
        if self._hdl is None:
            self._hdl = ffi.new('nvlist_t **')
        if self._alloc is True:
            self._alloced = libzfs.nvlist_alloc(self._hdl, int(self._flags), 0)
        return self._alloced
    __enter__ = alloc

    def free(self, exc_type=None, exc_val=None, exc_tb=None):
        if self._hdl and self._free and self._alloced:
            libzfs.nvlist_free(self.ptr)
            self._alloced = None
    __exit__ = free

    @property
    def ptr(self):
        if self._hdl:
            return self._hdl[0]
        return None

    @property
    def hdl(self):
        return self._hdl

    def add(self, key, data_type, value):
        info = self._detect_type(data_type)
        value = info.from_python(value)
        return not bool(info.nvlist_add(self.ptr, key, value))

    def lookup(self, key, data_type, default=NO_DEFAULT):
        info = self._detect_type(data_type)

        holder = info.new()
        countholder = None
        if info.is_array:
            countholder = ffi.new(HOLDER_TYPE)
            val = info.nvlist_lookup(self.ptr, key, holder, countholder)
        else:
            val = info.nvlist_lookup(self.ptr, key, holder)
        if not bool(val):
            return info.to_python(holder, countholder)
        elif default is not NO_DEFAULT:
            return default
        raise KeyError(key)

    def _lookup_type(self, key, default=NO_DEFAULT):
        holder = ffi.new('nvpair_t **')
        val = libzfs.nvlist_lookup_nvpair(self.ptr, key, holder)
        if bool(val):
            raise KeyError(key)
        typeid = libzfs.nvpair_type(holder[0])
        data_type = data_type_t_safe(typeid)
        if data_type is None and default is NO_DEFAULT:
            raise UnknownDataType("Unknown data id: %r" % typeid)
        elif data_type is None:
            data_type = default
        return data_type, typeid, holder

    def lookup_type(self, key):
        data_type, typeid, holder = self._lookup_type(key)
        return data_type

    def exists(self, key):
        return self._lookup_type(key, default=False)

    def lookup_smart(self, key, default=NO_DEFAULT):
        data_type = holder = None
        try:
            data_type, typeid, holder = self._lookup_type(key)
        except:
            pass

        if not data_type:
            if default is NO_DEFAULT:
                raise KeyError(key)
            return default

        info = self._detect_type(data_type)
        valholder = info.new()
        countholder = None
        if info.is_array:
            countholder = ffi.new(HOLDER_TYPE)
            val = info.nvpair_value(holder[0], valholder, countholder)
        else:
            val = info.nvpair_value(holder[0], valholder)
        if not bool(val):
            return info.to_python(valholder, countholder)
        elif default is NO_DEFAULT:
            raise KeyError(key)
        return default

    def _iter_nvlist(self, skip_unknown=False):
        pair = libzfs.nvlist_next_nvpair(self.ptr, ffi.NULL)
        while pair != ffi.NULL:
            key = ffi.string(libzfs.nvpair_name(pair))
            typeid = libzfs.nvpair_type(pair)
            data_type = data_type_t_safe(typeid)
            info = self._detect_type(data_type, default=None)
            if (data_type and info) or skip_unknown is False:
                yield pair, key, typeid, data_type, info
            pair = libzfs.nvlist_next_nvpair(self.ptr, pair)

    def items(self, skip_unknown=False, deep=20, extended=False):
        def y(k, t, v):
            if extended:
                return (k, t, v)
            return (k, v)

        for pair, key, typeid, data_type, info in self._iter_nvlist():
            if data_type is None or info is None:
                yield y(key, data_type, None)
            valholder = info.new()
            countholder = None
            if info.is_array:
                countholder = ffi.new(HOLDER_TYPE)
                val = info.nvpair_value(pair, valholder, countholder)
            else:
                val = info.nvpair_value(pair, valholder)
            if not bool(val):
                value = info.to_python(valholder, countholder)

                def _iter(item):
                    item._free = self._free
                    with item:
                        valtype = list if extended else dict
                        dictval = valtype(item.items(skip_unknown=skip_unknown, deep=deep - 1, extended=extended))
                    return dictval

                if deep > 0 and isinstance(value, NVList):
                    value = _iter(value)
                elif deep > 0 and isinstance(value, list) and isinstance(value[0], NVList):
                    value = [_iter(x) for x in value]

                yield y(key, data_type, value)
            pair = libzfs.nvlist_next_nvpair(self.ptr, pair)


class NVListHandler(object):
    def __init__(self, funcname, typename, converter, add_converter = None, is_array = False):
        self._funcname = funcname
        self._typename = typename
        self._converter = converter
        self._add_converter = add_converter
        self._is_array = is_array

    def new(self):
        return ffi.new(self._typename)

    def to_python(self, x, count = None):
        if self._converter:
            if self.is_array:
                return self._converter(x, count)
            return self._converter(x)
        return x

    def from_python(self, x):
        if callable(self._add_converter):
            return self._add_converter(x)
        if self._add_converter is False:
            raise Exception("Unable to convert type")
        return x

    def _get_libzfs_func(self, prefix):
        return getattr(libzfs, '%s_%s' % (prefix, self._funcname))

    @property
    def nvlist_add(self):
        return self._get_libzfs_func('nvlist_add')

    @property
    def nvlist_lookup(self):
        return self._get_libzfs_func('nvlist_lookup')

    @property
    def nvpair_value(self):
        return self._get_libzfs_func('nvpair_value')

    @property
    def is_array(self):
        return self._is_array


def _array_converter(converter):
    def _inner(x, count):
        items = []
        for i in range(count[0]):
            items.append(converter(x[0][i]))
        return items
    return _inner


def _to_int(hdl):
    if isinstance(hdl, six.integer_types):
        return int(hdl)
    return int(hdl[0])


#
# Key: configuration
#  - add func
#  - lookup func
#  - lookup holder type
#  - add converter
#  - lookup converter
#
NVLIST_HANDLERS = {
    data_type_t.DATA_TYPE_BOOLEAN:      NVListHandler('boolean_value', 'boolean_t *', lambda x: bool(x[0]), boolean_t),
    data_type_t.DATA_TYPE_BOOLEAN_VALUE: NVListHandler('boolean_value', 'boolean_t *', lambda x: bool(x[0]), boolean_t),
    data_type_t.DATA_TYPE_BYTE:         NVListHandler('byte', 'uchar_t *', _to_int, None),
    data_type_t.DATA_TYPE_INT8:         NVListHandler('int8', 'int8_t *', _to_int, None),
    data_type_t.DATA_TYPE_UINT8:        NVListHandler('uint8', 'uint8_t *', _to_int, None),
    data_type_t.DATA_TYPE_INT16:        NVListHandler('int16', 'int16_t *', _to_int, None),
    data_type_t.DATA_TYPE_UINT16:       NVListHandler('uint16', 'uint16_t *', _to_int, None),
    data_type_t.DATA_TYPE_INT32:        NVListHandler('int32', 'int32_t *', _to_int, None),
    data_type_t.DATA_TYPE_UINT32:       NVListHandler('uint32', 'uint32_t *', _to_int, None),
    data_type_t.DATA_TYPE_INT64:        NVListHandler('int64', 'int64_t *', _to_int, None),
    data_type_t.DATA_TYPE_UINT64:       NVListHandler('uint64', 'uint64_t *', _to_int, None),
    data_type_t.DATA_TYPE_STRING:       NVListHandler('string', 'char **', lambda x: ffi.string(x[0]), None),
    data_type_t.DATA_TYPE_NVLIST:       NVListHandler('nvlist', 'nvlist_t **', NVList.from_nvlist_hdl, False),

    data_type_t.DATA_TYPE_BYTE_ARRAY:   NVListHandler('byte_array', 'uchar_t **', _array_converter(_to_int), None),
    data_type_t.DATA_TYPE_INT8_ARRAY:   NVListHandler('int8_array', 'int8_t **', _array_converter(_to_int), False, True),
    data_type_t.DATA_TYPE_UINT8_ARRAY:  NVListHandler('uint8_array', 'uint8_t **', _array_converter(_to_int), False, True),
    data_type_t.DATA_TYPE_INT16_ARRAY:  NVListHandler('int16_array', 'int16_t **', _array_converter(_to_int), False, True),
    data_type_t.DATA_TYPE_UINT16_ARRAY: NVListHandler('uint16_array', 'uint16_t **', _array_converter(_to_int), False, True),
    data_type_t.DATA_TYPE_INT32_ARRAY:  NVListHandler('int32_array', 'int32_t **', _array_converter(_to_int), False, True),
    data_type_t.DATA_TYPE_UINT32_ARRAY: NVListHandler('uint32_array', 'uint32_t **', _array_converter(_to_int), False, True),
    data_type_t.DATA_TYPE_INT64_ARRAY:  NVListHandler('int64_array', 'int64_t **', _array_converter(_to_int), False, True),
    data_type_t.DATA_TYPE_UINT64_ARRAY: NVListHandler('uint64_array', 'uint64_t **', _array_converter(_to_int), False, True),
    data_type_t.DATA_TYPE_NVLIST_ARRAY: NVListHandler('nvlist_array', 'nvlist_t ***',
                                        _array_converter(NVList.from_nvlist_ptr), False, True),
    data_type_t.DATA_TYPE_STRING_ARRAY: NVListHandler('string_array', 'char ***',
                                        _array_converter(lambda x: ffi.string(x)), False, True),
}
