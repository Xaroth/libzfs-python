import unittest
import random
import string

from nose.tools import *

from libzfs.nvpair import NVList, data_type


class Test_libnvpair(unittest.TestCase):
    def test_001_add_lookup_int(self):
        data = random.randint(1, 65535)
        dt = data_type.UINT64
        print "Random data: %r" % data

        nvlist = NVList()
        with nvlist:
            print "Adding:", nvlist.add('test', dt, data)
            found = nvlist.lookup('test', dt, -1)
            print "Found:", found
            assert found == data

    def test_002_add_lookup_string(self):
        length = random.randint(32, 128)
        data = ''.join([random.choice(string.ascii_letters) for x in range(length)])
        dt = data_type.STRING
        print "Random data: %r" % data

        nvlist = NVList()
        with nvlist:
            print "Adding:", nvlist.add('test', dt, data)
            found = nvlist.lookup('test', dt, -1)
            print "Found:", found
            assert data == found

    def test_003_add_lookup_bool(self):
        data = bool(random.randint(0, 1))
        dt = data_type.BOOLEAN
        print "Random data: %r" % data

        nvlist = NVList()
        with nvlist:
            print "Adding:", nvlist.add('test', dt, data)
            found = nvlist.lookup('test', dt, -1)
            print "Found:", found
            assert data == found

    def test_004_add_lookup_smart(self):
        length = random.randint(32, 128)
        items = {
            'int': [random.randint(1, 65535), data_type.UINT64],
            'string': [''.join([random.choice(string.ascii_letters) for x in range(length)]), data_type.STRING],
            'bool': [bool(random.randint(0, 1)), data_type.BOOLEAN]
        }

        nvlist = NVList()
        with nvlist:
            print "Adding items"
            for iname, data in items.items():
                nvlist.add(iname, data[1], data[0])
            print "Retreiving items"
            for iname, data in items.items():
                print "Checking: %s ( %r )" % (iname, data[0])
                value = nvlist.lookup_smart(iname, default=-1)
                assert value == data[0]

    @raises(KeyError)
    def test_005_lookup_unknown_key(self):
        nvlist = NVList()
        with nvlist:
            nvlist.lookup_smart('this_key_should_not_be_available')

    def test_006_lookup_defaulting(self):
        nvlist = NVList()
        default = random.randint(32, 128)
        with nvlist:
            found = nvlist.lookup_smart('this_key_should_not_be_available', default=default)
            assert found == default
