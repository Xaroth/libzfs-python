import unittest

from libzfs import LibZFSHandle


class Test_LibZFSHandle(unittest.TestCase):
    def test_001_context_manager(self):
        with LibZFSHandle():
            pass

    def test_002_manual(self):
        LibZFSHandle.init()

        LibZFSHandle.fini()
