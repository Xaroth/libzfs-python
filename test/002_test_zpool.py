import unittest
import os
from .test_utils import _LibZFSHandleCase
from libzfs.zpool import ZPool, zpool_prop_t
from libzfs import bindings

LIBZFS_TEST_POOL = os.environ.get("LIBZFS_TEST_POOL", False)


@unittest.skipUnless(LIBZFS_TEST_POOL, "LIBZFS_TEST_POOL not set, so we do not test to a specific pool")
class Test_ZPool(_LibZFSHandleCase):
    def test_001_iter_zpools(self):
        pools = ZPool.list()
        assert len(pools) > 0

    def test_002_get_zpool(self):
        pool = ZPool.get(name=LIBZFS_TEST_POOL)
        assert pool is not None

    def test_003_get_zpool_properties(self):
        pool = ZPool.get(name=LIBZFS_TEST_POOL)
        props = pool.properties
        assert len(props.keys()) > 0
        assert props.get(zpool_prop_t.ZPOOL_PROP_NAME) == LIBZFS_TEST_POOL
        assert props.get(zpool_prop_t.ZPOOL_PROP_SIZE) > 0

    def test_004_get_zpool_properties_easy_access(self):
        pool = ZPool.get(name=LIBZFS_TEST_POOL)
        props = pool.properties
        assert props.name == props.get(zpool_prop_t.ZPOOL_PROP_NAME, None)
        assert props.size == props.get(zpool_prop_t.ZPOOL_PROP_SIZE, None)

    def test_005_get_zpool_config(self):
        pool = ZPool.get(name=LIBZFS_TEST_POOL)
        config = pool.config
        pool.refresh_stats()
        oldconfig = pool.old_config
        assert len(config.keys()) > 0
        assert len(oldconfig.keys()) > 0
        assert config == oldconfig

    def test_006_get_zpool_config_easy_access(self):
        from datetime import datetime
        pool = ZPool.get(name=LIBZFS_TEST_POOL)
        config = pool.config
        assert isinstance(config.initial_load_time, datetime)
        assert config.name == config.get(bindings['ZPOOL_CONFIG_POOL_NAME'], None)
