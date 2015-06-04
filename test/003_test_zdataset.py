import unittest
import os
from .test_utils import _LibZFSHandleCase
from libzfs.zdataset import ZDataset, zfs_prop_t, libzfs, ffi

LIBZFS_TEST_POOL = os.environ.get("LIBZFS_TEST_POOL", False)


@unittest.skipUnless(LIBZFS_TEST_POOL, "LIBZFS_TEST_POOL not set, so we do not test to a specific pool")
class Test_ZDataset(_LibZFSHandleCase):
    def test_001_iter_zdatasets(self):
        datasets = ZDataset.list()
        assert len(datasets) > 0

    def test_002_get_zdataset(self):
        dataset = ZDataset.get(name=LIBZFS_TEST_POOL)
        assert dataset is not None

    def test_003_get_zdataset_properties(self):
        dataset = ZDataset.get(name=LIBZFS_TEST_POOL)
        props = dataset.properties

        dstype = dataset.type
        dstype_name = ffi.string(libzfs.zfs_type_to_name(dstype))

        assert len(props.keys()) > 0
        assert props.get(zfs_prop_t.ZFS_PROP_NAME) == LIBZFS_TEST_POOL
        assert props.get(zfs_prop_t.ZFS_PROP_TYPE) == dstype_name

    def test_004_get_zdataset_children(self):
        dataset = ZDataset.get(name=LIBZFS_TEST_POOL)
        assert dataset.children is not None
        assert dataset.child_filesystems is not None
        assert dataset.child_snapshots is not None
