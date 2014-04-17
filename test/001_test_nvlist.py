import unittest
import random
import string

from libzfs.nvpair import NVList


class Test_libnvpair(unittest.TestCase):
    def test_add_lookup_int(self):
        data = random.randint(1, 65535)
        print "Random data: %r" % data

        nvlist = NVList()
        with nvlist:
            print "Adding:", nvlist.add('test', data)
            found = nvlist.lookup('test', int, -1)
            print "Found:", found
            assert found == data

    def test_add_lookup_string(self):
        length = random.randint(32, 128)
        data = ''.join([random.choice(string.ascii_letters) for x in range(length)])
        print "Random data: %r" % data

        nvlist = NVList()
        with nvlist:
            print "Adding:", nvlist.add('test', data)
            found = nvlist.lookup('test', str, -1)
            print "Found:", found
            assert data == found

    def test_add_lookup_bool(self):
        data = bool(random.randint(0, 1))
        print "Random data: %r" % data

        nvlist = NVList()
        with nvlist:
            print "Adding:", nvlist.add('test', data)
            found = nvlist.lookup('test', bool, -1)
            print "Found:", found
            assert data == found
