from __future__ import absolute_import
import logging
import os
uname = os.uname()[0].lower()

from cffi import FFI

from .generic import TYPEDEFS, FUNCTIONS, INCLUDES, GENERATE, verify
from ..utils.recursivedict import RecursiveDictionary


class BindingManager(object):
    def __init__(self):
        self.log = logging.getLogger('%s.%s' % (self.__class__.__module__, self.__class__.__name__))
        self._functions = RecursiveDictionary()
        self._typedefs = RecursiveDictionary()
        self._includes = RecursiveDictionary()
        self._generate = RecursiveDictionary()
        self._verifier = None

    def include(self, functions=None, typedefs=None, includes=None, generate=None, verifier=None):
        if functions:
            self._functions.rec_update(functions)
        if typedefs:
            self._typedefs.rec_update(typedefs)
        if includes:
            self._includes.rec_update(includes)
        if generate:
            self._generate.rec_update(generate)
        if verifier:
            self._verifier = verifier

    def generate_item(self, item):
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
        self.log.debug("CDef: typedefs")
        ffi.cdef('\n'.join(line for line in typedefs.values() if line))
        self.log.debug("CDef: functions")
        ffi.cdef('\n'.join(line for line in functions.values() if line))

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
manager.include(FUNCTIONS, TYPEDEFS, INCLUDES, GENERATE, verify)

if 'linux' in uname:
    from .unix import (TYPEDEFS as TD_UNIX,
                       FUNCTIONS as FN_UNIX,
                       INCLUDES as INC_UNIX,
                       verify as verify_UNIX,
                       GENERATE as GEN_UNIX)
    manager.log.info("Loading unix-specific information")
    manager.include(FN_UNIX, TD_UNIX, INC_UNIX, GEN_UNIX, verify_UNIX)
elif 'freebsd' in uname:
    manager.log.info("Loading bsd-specific information")
elif 'darwin' in uname:
    manager.log.info("Loading osx-specific information")
manager.generate()
