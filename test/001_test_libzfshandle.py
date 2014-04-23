import unittest

from libzfs import LibZFSHandle


class Test_LibZFSHandle(unittest.TestCase):
    def test_001_context_manager(self):
        with LibZFSHandle():
            pass

    def test_002_manual(self):
        LibZFSHandle.init()

        LibZFSHandle.fini()

    def test_003_multiple(self):
        with LibZFSHandle() as ptr:
            ptr2 = LibZFSHandle.init()
            refcount = LibZFSHandle.refcount()
            LibZFSHandle.fini()

            assert refcount > 1
            assert ptr == ptr2
            assert LibZFSHandle.refcount() == (refcount - 1)
