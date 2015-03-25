import unittest
from libzfs.handle import LibZFSHandle


class _LibZFSHandleCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LibZFSHandle.init()

    @classmethod
    def tearDownClass(cls):
        LibZFSHandle.fini()

    def setUp(self):
        LibZFSHandle.init()

    def tearDown(self):
        LibZFSHandle.fini()
