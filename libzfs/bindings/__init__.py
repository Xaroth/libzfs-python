from __future__ import absolute_import
import logging
import os
from pkg_resources import parse_version
try:
    uname = os.uname()[0].lower()
except AttributeError:
    # uname is not available, we're most likely running on a non-unix-like system
    # (aka windows)
    uname = 'unknown'

from .generic import TYPEDEFS, FUNCTIONS, INCLUDES, GENERATE, VERSION_SPECIFIC, verify
from ..utils.recursivedict import RecursiveDictionary


class BindingManager(object):
    def __init__(self):
        self.log = logging.getLogger('%s.%s' % (self.__class__.__module__, self.__class__.__name__))
        self._functions = RecursiveDictionary()
        self._typedefs = RecursiveDictionary()
        self._includes = RecursiveDictionary()
        self._generate = RecursiveDictionary()
        self._version_specific = RecursiveDictionary()
        self._verifier = None

    def include(self, functions=None, typedefs=None, includes=None, generate=None, version_specific=None,
                verifier=None):
        if functions:
            self._functions.rec_update(functions)
        if typedefs:
            self._typedefs.rec_update(typedefs)
        if includes:
            self._includes.rec_update(includes)
        if generate:
            self._generate.rec_update(generate)
        if version_specific:
            self._version_specific.rec_update(version_specific)
        if verifier:
            self._verifier = verifier

    def process_defs(self, defs, version_specific):
        from .. import libzfs_version
        installed_version = parse_version(libzfs_version)
        ignorelist = []
        for key, items in version_specific.items():
            version = parse_version(key)
            if version > installed_version:
                self.log.info("Ignoring version '%s' as it is newer than our installed version (%s)",
                              key, libzfs_version)
                ignorelist.extend(items)

        ignorelist = set(ignorelist)
        return [line for key, line in defs.items() if line and key not in ignorelist]

    def generate_item(self, item):
        from cffi import FFI

        if item in self.items:
            self.log.info("'%s' already generated", item)
            return self.items[item], self.ffi[item]
        if item in self.building:
            raise Exception("Recursion loop detected: building: '%s'" % (', '.join(self.building)))
        includes = self._includes.get(item)
        ffi = FFI()
        for inc in includes:
            self.log.debug("Checking for include: '%s'", inc)
            generated, inc_ffi = self.generate_item(inc)
            ffi.include(inc_ffi)

        functions = self._functions.get(item)
        typedefs = self._typedefs.get(item)
        do_generate = self._generate.get(item, False)
        version_specific = self._version_specific.get(item, {})
        self.log.debug("CDef: typedefs")
        ffi.cdef('\n'.join(self.process_defs(typedefs, version_specific)))
        self.log.debug("CDef: functions")
        ffi.cdef('\n'.join(self.process_defs(functions, version_specific)))

        if do_generate:
            self.log.info("Verifying: '%s'", item)
            generated = self._verifier(ffi)
        else:
            self.log.info("Skipping verify for: '%s'", item)
            generated = None
        self.log.debug("Done with '%s'", item)
        self.items[item] = generated
        self.ffi[item] = ffi
        return generated, ffi

    def mock_accessors(self):
        self.log.info('Mocking the accessors for our cffi libraries.')
        keys = set(self._functions.keys()) | set(self._typedefs.keys())
        self.items = {}
        self.ffi = {}
        for item in keys:
            setattr(self, item, None)
            setattr(self, '%s_ffi' % item, None)

    def generate(self):
        self.log.info("Generating all modules")
        keys = set(self._functions.keys()) | set(self._typedefs.keys())

        self.items = {}
        self.ffi = {}
        self.building = []

        for item in keys:
            self.log.info("Generating: '%s'", item)
            generated, ffi = self.generate_item(item)
            if generated:
                setattr(self, item, generated)
            setattr(self, '%s_ffi' % item, ffi)

    def get_extensions(self):
        modules = [ffi for key, ffi in self.ffi.items() if self.items.get(key, False)]
        return [ffi.verifier.get_extension() for ffi in modules]

manager = BindingManager()
manager.include(FUNCTIONS, TYPEDEFS, INCLUDES, GENERATE, VERSION_SPECIFIC, verify)

if 'linux' in uname:
    from .unix import (TYPEDEFS as TD_UNIX,
                       FUNCTIONS as FN_UNIX,
                       INCLUDES as INC_UNIX,
                       verify as verify_UNIX,
                       GENERATE as GEN_UNIX,
                       VERSION_SPECIFIC as VS_UNIX)
    manager.log.info("Loading unix-specific information")
    manager.include(FN_UNIX, TD_UNIX, INC_UNIX, GEN_UNIX, VS_UNIX, verify_UNIX)
elif 'freebsd' in uname:
    manager.log.info("Loading bsd-specific information")
elif 'darwin' in uname:
    manager.log.info("Loading osx-specific information")

if os.environ.get('MOCK_CFFI', False) != '1':
    manager.generate()
else:
    manager.mock_accessors()


__all__ = [
    'manager',
]
