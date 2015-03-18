import copy
from cffi import FFI
from enum import IntEnum
import json
import operator
import os
from os.path import join, dirname, abspath, exists
import re
import subprocess

from .utils import six

CURRENT_DIR = dirname(abspath(__file__))

# Shift values for enums, a-la:
# {
#    FIRST_VALUE = 1 << 1,
#    SECOND_VALUE = 1 << 2,
# }
# etc etc. also supports the usage of letters ('Z' << 2), or addition.
RX_SHIFT = re.compile(r'(\(?(?:[0-9A-Fx]+|\'\w+\')\)?)\s*((?:<<)|(?:>>)|(?:\|)|(?:\+)|(?:\-))\s*(\(?[0-9A-Fx]+\)?)')
RX_SHIFT_COMPLEX = re.compile(r'(\(?(?:[0-9A-FxUL]+|[\w\'\"]+)\)?)\s*((?:<<)|(?:>>)|(?:\|)|(?:\+)|(?:\-))\s*(\(?(?:[0-9A-FxUL]+|[\w\'\"]+)\)?)')
# Array dimensioning containing simple math
# i.e. char *test[6+1]
AR_DIM = re.compile(r'(\d+)\s*((?:<<)|(?:>>)|(?:\|)|(?:\+)|(?:\-))\s*(\d+)')
# The operators we allow in the above two cases
OPERATORS = {
    '<<': operator.lshift,
    '|': operator.or_,
    '>>': operator.rshift,
    '+': operator.add,
    '-': operator.sub,
}

IS_INTEGER_VALUE = re.compile(r'^([0-9A-F.eEx\+\-LU]+)$')


def _to_int(x):
    try:
        return int(x)
    except ValueError:
        return int(x, 16)


def shift_replace(m):
    left, shift, right = m.group(1).lstrip('('), m.group(2), m.group(3).rstrip(')')
    left = left.strip()
    right = right.strip()
    if left[0] == left[-1] and left[0] in ("'", '"'):
        left = ord(left[1:-1])
    else:
        left = _to_int(left)
    if right[0] == right[-1] and right[0] in ("'", '"'):
        right = ord(right[1:-1])
    else:
        right = _to_int(right)

    shift = shift.strip()
    op = OPERATORS.get(shift)
    if not op:
        return KeyError(shift)
    return str(op(left, right))


def shift_replace_complex(items):
    def _inner(m):
        left, shift, right = m.group(1).lstrip('('), m.group(2), m.group(3).rstrip(')')
        left = left.strip()
        right = right.strip()
        shift = shift.strip()
        if left[0] == left[-1] and left[0] in ("'", '"'):
            left = ord(left[1:-1])
        else:
            if IS_INTEGER_VALUE.match(left):
                left = _to_int(left.rstrip('UL'))
            elif left in items:
                left = items[left]
                return str('(%s %s %s)' % (left, shift, right))
            else:
                return ''
        if right[0] == right[-1] and right[0] in ("'", '"'):
            right = ord(right[1:-1])
        else:
            if IS_INTEGER_VALUE.match(right):
                right = _to_int(right.rstrip('UL'))
            elif right in items:
                right = items[right]
                return str('(%s %s %s)' % (left, shift, right))
            else:
                return ''
        op = OPERATORS.get(shift)
        if not op:
            return KeyError(shift)
        return str(op(left, right))
    return _inner

# Simple regex to locate function definitions
FUNCTION_REGEX = re.compile(r'(.*)\s([\w*]+)\(')


class BindingManager(object):
    DEFAULT_VERIFY_INCLUDE_DIRS = [
        '/usr/include/libzfs',
        '/usr/include/libspl',
    ]

    DEFAULT_GENERATE_INCLUDE_DIRS = DEFAULT_VERIFY_INCLUDE_DIRS + [
        join(CURRENT_DIR, 'bindings', 'fake-includes'),
    ]

    DEFAULT_DEFINES = [
        ('NDEBUG', 1),
        ('HAVE_IOCTL_IN_SYS_IOCTL_H', 1),
    ]

    DEFAULT_FUNCTION_BLACKLIST = [
        'libzfs_fru_lookup',        # !HAVE_LIBTOPO
        'libzfs_fru_devpath',       # !HAVE_LIBTOPO
        'libzfs_fru_compare',       # !HAVE_LIBTOPO
        'libzfs_fru_notself',       # !HAVE_LIBTOPO
        'libzfs_fru_refresh',       # !HAVE_LIBTOPO
        'zpool_fru_set',            # !HAVE_LIBTOPO

        'zfs_deleg_share_nfs',      # Not implemented
        'zfs_get_recvd_props',      # Not implemented
        'zfs_prop_get_feature',     # Not implemented
    ]

    DEFAULT_SOURCE = """
#define __attribute__(x)
#include <libzfs.h>
"""
    DEFAULT_VERIFY = """
#include <libzfs.h>
#include <libnvpair.h>
#include <sys/fs/zfs.h>
#include <sys/types.h>
"""
    DEFAULT_LIBRARIES = [
        'zfs',
        'nvpair',
        'zpool',
    ]

    TYPEDEF_ENUM = 'typedef enum'
    TYPEDEF_ENUM_LEN = len(TYPEDEF_ENUM)

    DEFAULT_OUTPUT = join(CURRENT_DIR, 'bindings', 'output')

    def __init__(self, parameters=None):
        if parameters is None:
            parameters = {}
        self.parameters = parameters
        self._ffi = None
        self._libzfs = None
        self._defines = {}
        self._undefines = []
        self._enums = {}

    def _merge_with_environ(self, defaults, environ_name, params_name):
        base = defaults[:]
        extra = os.environ.get(environ_name)
        params = self.parameters.get(params_name)

        if extra:
            extra = extra.split(',')
            extra.reverse()
        if params:
            if not isinstance(params, list):
                params = [params]
        if extra or params:
            base.reverse()
            base.extend(params or [])
            base.extend(extra or [])
            base.reverse()
        return base

    def get_defined_params(self):
        return self._merge_with_environ(self.DEFAULT_DEFINES, 'LIBZFS_EXTRA_DEFINES', 'defines')

    def build_compile_command(self):
        command = ['gcc', '-E', '-std=c89', '-xc-header', '-dD']
        command.extend(['-I%s' % x for x in self._merge_with_environ(self.DEFAULT_GENERATE_INCLUDE_DIRS,
                                                                     'LIBZFS_EXTRA_GENERATE_INCLUDE_DIRS',
                                                                     'generate_include_dirs')])
        command.extend(['-D%s=%s' % (x, y) for x, y in self.get_defined_params()])
        command.extend(self._merge_with_environ([], 'LIBZFS_EXTRA_GCC_PARAMS', 'gcc_params'))
        command.append('-')
        return command

    def process_enum_line(self, line):
        while RX_SHIFT.search(line):
            line = RX_SHIFT.sub(shift_replace, line, 1)
        if line.startswith(self.TYPEDEF_ENUM):
            # We now know absolutely sure it's an enum
            data, name = line.rsplit('}', 1)
            prefix, data = data.split('{', 1)

            name = name.rstrip(';').strip()
            prefix = prefix.strip()
            items = []
            for part in data.split(','):
                if '=' in part:
                    part = part[:part.index('=')]
                items.append(part.strip())
            self._enums[name] = items
        return line

    def process_define_line(self, line):
        parts = line.split(' ', 2) + [None, None, None]
        process_type, name, value = parts[:3]
        if process_type == '#define':
            self._defines[name] = value
        elif process_type == '#undef':
            self._undefines.append(name)

    def process_array_line(self, line):
        while AR_DIM.search(line):
            line = AR_DIM.sub(shift_replace, line, 1)
        return line

    def process_headers(self, output):
        output_dir = os.environ.get('LIBZFS_OUTPUT', self.DEFAULT_OUTPUT)
        headers_raw_path = join(output_dir, 'headers.h.in')
        with open(headers_raw_path, 'w') as fh:
            fh.write(output)
        function_blacklist = self._merge_with_environ(self.DEFAULT_FUNCTION_BLACKLIST,
                                                      'LIBZFS_FUNCTION_BLACKLIST',
                                                      'blacklist')
        # First we reduce enums to a single line, and replace all tabs with spaces
        output = output.replace(',\n', ', ').replace('\n}', '}').replace('\t', ' ')
        # Now we remove double newlines and double spaces
        output = re.sub('\s\s+', ' ', re.sub('\n\n+', '\n', output))
        previous = None
        for line in output.splitlines():
            if not line:
                continue
            if line.startswith('# ') or line.startswith('//'):  # Comments
                continue
            if previous:
                line = previous + ' ' + line
                previous = None
            line = line.strip()
            # Check if we're dealing with a define
            if line.startswith('#'):
                self.process_define_line(line)
                continue
            if not line.endswith(';') and not line.endswith('}'):
                previous = line
                continue
            # Check if we're dealing with a function
            func_match = FUNCTION_REGEX.match(line)
            if func_match and func_match.group(2).lstrip('*') in function_blacklist:
                continue
            if func_match and 'inline' in func_match.group(1):
                continue
            # Check if we're dealing with an enum line
            if '=' in line and '==' not in line:
                line = self.process_enum_line(line)
            # Check if we have an array def in this line
            if '[' in line and ']' in line:
                line = self.process_array_line(line)
            if not line:
                continue
            yield line

    def build_headers(self):
        self._defines = {}
        self._undefines = []
        self._enums = {}
        build_source = six.binary_type(self.parameters.get('build_source', self.DEFAULT_SOURCE))
        process = subprocess.Popen(self.build_compile_command(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, _ = process.communicate(build_source)
        return '\n'.join(self.process_headers(stdout))

    def build_defines(self):
        items = copy.copy(self._defines)

        def _get(x):
            y = x
            if x[0] == '(' and x[-1] == ')':
                x = x[1:-1]
            if x in items:
                found = items[x]
                if found != x:
                    return _get(found)
            if not x.startswith('__'):
                x = '__%s__' % x
                magic = _get(x)
                if magic != x:
                    return magic
            return y
        processed_defines = {key: _get(value) for key, value in six.iteritems(self._defines)}

        for key, value in six.iteritems(processed_defines):
            if IS_INTEGER_VALUE.match(value):
                val = value.rstrip('UL')
                try:
                    value = _to_int(val)
                except ValueError:
                    try:
                        value = float(val)
                    except:
                        continue
                yield key, value
            elif len(value) > 1 and value[0] == value[-1] and value[0] in ("'", '"'):
                yield key, value[1:-1]
            elif RX_SHIFT_COMPLEX.search(value):
                # This is probably a complex variable.
                replacer = shift_replace_complex(processed_defines)
                while RX_SHIFT_COMPLEX.search(value):
                    value = RX_SHIFT_COMPLEX.sub(replacer, value, 1)
                if value:
                    yield key, value
            else:
                # This is most likely a complex value or macro, so we ignore these (for now)
                pass

    def build(self):
        headers = self.build_headers()
        defines = dict(self.build_defines())
        enums = self._enums

        output_dir = os.environ.get('LIBZFS_OUTPUT', self.DEFAULT_OUTPUT)
        headers_path = join(output_dir, 'headers.h')
        defines_path = join(output_dir, 'defines.json')
        enums_path = join(output_dir, 'enums.json')

        with open(defines_path, 'w') as fh:
            json.dump(defines, fh, sort_keys=True, indent=4 if os.environ.get('LIBZFS_SANE_JSON') else None)
        with open(enums_path, 'w') as fh:
            json.dump(self._enums, fh, sort_keys=True, indent=4 if os.environ.get('LIBZFS_SANE_JSON') else None)
        with open(headers_path, 'w') as fh:
            fh.write(headers)
        return headers, defines, enums

    def compile(self, headers=None, defines=None, enums=None):
        output_dir = os.environ.get('LIBZFS_OUTPUT', self.DEFAULT_OUTPUT)
        headers_path = join(output_dir, 'headers.h')
        defines_path = join(output_dir, 'defines.json')
        enums_path = join(output_dir, 'enums.json')

        if not headers and exists(headers_path):
            with open(headers_path, 'r') as fh:
                headers = fh.read()
        if not defines and exists(defines_path):
            with open(defines_path, 'r') as fh:
                defines = json.load(fh)
        if not enums and exists(enums_path):
            with open(enums_path, 'r') as fh:
                enums = json.load(fh)

        regenerate = os.environ.get('LIBZFS_REGENERATE') or self.parameters.get('regenerate')

        if not headers or not defines or not enums or regenerate:
            headers, defines, enums = self.build()

        ffi = FFI()
        ffi.cdef(headers, override=True)
        return ffi, defines, enums

    @property
    def ffi(self):
        if self._ffi:
            return self._ffi
        self._ffi, self._defines, self._enums = self.compile()
        return self._ffi

    @property
    def libzfs(self):
        if self._libzfs:
            return self._libzfs
        verify = six.binary_type(self.parameters.get('verify_source', self.DEFAULT_VERIFY))
        libraries = self._merge_with_environ(self.DEFAULT_LIBRARIES, 'LIBZFS_LIBRARIES', 'libraries')
        includes = self._merge_with_environ(self.DEFAULT_VERIFY_INCLUDE_DIRS,
                                            'LIBZFS_EXTRA_VERIFY_INCLUDE_DIRS',
                                            'verify_include_dirs')
        macros = self.get_defined_params()
        ffi = self.ffi
        self._libzfs = ffi.verify(verify, define_macros=macros, include_dirs=includes, libraries=libraries)
        return self._libzfs

    @property
    def defines(self):
        if self._defines:
            return self._defines
        self._ffi, self._defines, self._enums = self.compile()
        return self._defines

    @property
    def enums(self):
        if self._enums:
            return self._enums
        self._ffi, self._defines, self._enums = self.compile()
        return self._enums

    def __getitem__(self, key):
        defines = self.defines
        libzfs = self.libzfs

        if key in defines:
            return defines[key]
        if key in self.enums:
            keys = self.enums[key]
            return IntEnum(key, [[x, getattr(libzfs, x, 0)] for x in keys])
        if hasattr(libzfs, key):
            val = getattr(libzfs, key)
            if isinstance(val, six.string_types + six.integer_types):
                return val
        raise KeyError(key)

default_manager = BindingManager()
