from __future__ import absolute_import
from enum import IntEnum

zfs_error = IntEnum("zfs_error", [
    ("SUCCESS",         0),  # no error -- success
    ("NOMEM",           2000),  # out of memory
    ("BADPROP",         2001),  # invalid property value
    ("PROPREADONLY",    2002),  # cannot set readonly property
    ("PROPTYPE",        2003),  # property does not apply to dataset type
    ("PROPNONINHERIT",  2004),  # property is not inheritable
    ("PROPSPACE",       2005),  # bad quota or reservation
    ("BADTYPE",         2006),  # dataset is not of appropriate type
    ("BUSY",            2007),  # pool or dataset is busy
    ("EXISTS",          2008),  # pool or dataset already exists
    ("NOENT",           2009),  # no such pool or dataset
    ("BADSTREAM",       2010),  # bad backup stream
    ("DSREADONLY",      2011),  # dataset is readonly
    ("VOLTOOBIG",       2012),  # volume is too large for 32-bit system
    ("INVALIDNAME",     2013),  # invalid dataset name
    ("BADRESTORE",      2014),  # unable to restore to destination
    ("BADBACKUP",       2015),  # backup failed
    ("BADTARGET",       2016),  # bad attach/detach/replace target
    ("NODEVICE",        2017),  # no such device in pool
    ("BADDEV",          2018),  # invalid device to add
    ("NOREPLICAS",      2019),  # no valid replicas
    ("RESILVERING",     2020),  # currently resilvering
    ("BADVERSION",      2021),  # unsupported version
    ("POOLUNAVAIL",     2022),  # pool is currently unavailable
    ("DEVOVERFLOW",     2023),  # too many devices in one vdev
    ("BADPATH",         2024),  # must be an absolute path
    ("CROSSTARGET",     2025),  # rename or clone across pool or dataset
    ("ZONED",           2026),  # used improperly in local zone
    ("MOUNTFAILED",     2027),  # failed to mount dataset
    ("UMOUNTFAILED",    2028),  # failed to unmount dataset
    ("UNSHARENFSFAILED", 2029),  # unshare(1M) failed
    ("SHARENFSFAILED",  2030),  # share(1M) failed
    ("PERM",            2031),  # permission denied
    ("NOSPC",           2032),  # out of space
    ("FAULT",           2033),  # bad address
    ("IO",              2034),  # I/O error
    ("INTR",            2035),  # signal received
    ("ISSPARE",         2036),  # device is a hot spare
    ("INVALCONFIG",     2037),  # invalid vdev configuration
    ("RECURSIVE",       2038),  # recursive dependency
    ("NOHISTORY",       2039),  # no history object
    ("POOLPROPS",       2040),  # couldn't retrieve pool props
    ("POOL_NOTSUP",     2041),  # ops not supported for this type of pool
    ("POOL_INVALARG",   2042),  # invalid argument for this pool operation
    ("NAMETOOLONG",     2043),  # dataset name is too long
    ("OPENFAILED",      2044),  # open of device failed
    ("NOCAP",           2045),  # couldn't get capacity
    ("LABELFAILED",     2046),  # write of label failed
    ("BADWHO",          2047),  # invalid permission who
    ("BADPERM",         2048),  # invalid permission
    ("BADPERMSET",      2049),  # invalid permission set name
    ("NODELEGATION",    2050),  # delegated administration is disabled
    ("UNSHARESMBFAILED", 2051),  # failed to unshare over smb
    ("SHARESMBFAILED",  2052),  # failed to share over smb
    ("BADCACHE",        2053),  # bad cache file
    ("ISL2CACHE",       2054),  # device is for the level 2 ARC
    ("VDEVNOTSUP",      2055),  # unsupported vdev type
    ("NOTSUP",          2056),  # ops not supported on this dataset
    ("ACTIVE_SPARE",    2057),  # pool has active shared spare devices
    ("UNPLAYED_LOGS",   2058),  # log device has unplayed logs
    ("REFTAG_RELE",     2059),  # snapshot release: tag not found
    ("REFTAG_HOLD",     2060),  # snapshot hold: tag already exists
    ("TAGTOOLONG",      2061),  # snapshot hold/rele: tag too long
    ("PIPEFAILED",      2062),  # pipe create failed
    ("THREADCREATEFAILED", 2063),  # thread create failed
    ("POSTSPLIT_ONLINE", 2064),  # onlining a disk after splitting it
    ("SCRUBBING",       2065),  # currently scrubbing
    ("NO_SCRUB",        2066),  # no active scrub
    ("DIFF",            2067),  # general failure of zfs diff
    ("DIFFDATA",        2068),  # bad zfs diff data
    ("POOLREADONLY",    2069),  # pool is in read-only mode
    ("UNKNOWN",         2070),
])

zfs_type = IntEnum("zfs_type", [
    ("FILESYSTEM",      0x1),
    ("SNAPSHOT",        0x2),
    ("VOLUME",          0x4),
    ("POOL",            0x8),
])

zfs_prop = IntEnum("zfs_prop", [
    ('TYPE',            0),
    ('CREATION',        1),
    ('USED',            2),
    ('AVAILABLE',       3),
    ('REFERENCED',      4),
    ('COMPRESSRATIO',   5),
    ('MOUNTED',         6),
    ('ORIGIN',          7),
    ('QUOTA',           8),
    ('RESERVATION',     9),
    ('VOLSIZE',         10),
    ('VOLBLOCKSIZE',    11),
    ('RECORDSIZE',      12),
    ('MOUNTPOINT',      13),
    ('SHARENFS',        14),
    ('CHECKSUM',        15),
    ('COMPRESSION',     16),
    ('ATIME',           17),
    ('DEVICES',         18),
    ('EXEC',            19),
    ('SETUID',          20),
    ('READONLY',        21),
    ('ZONED',           22),
    ('SNAPDIR',         23),
    ('PRIVATE',         24),
    ('ACLINHERIT',      25),
    ('CREATETXG',       26),
    ('NAME',            27),
    ('CANMOUNT',        28),
    ('ISCSIOPTIONS',    29),
    ('XATTR',           30),
    ('NUMCLONES',       31),
    ('COPIES',          32),
    ('VERSION',         33),
    ('UTF8ONLY',        34),
    ('NORMALIZE',       35),
    ('CASE',            36),
    ('VSCAN',           37),
    ('NBMAND',          38),
    ('SHARESMB',        39),
    ('REFQUOTA',        40),
    ('REFRESERVATION',  41),
    ('GUID',            42),
    ('PRIMARYCACHE',    43),
    ('SECONDARYCACHE',  44),
    ('USEDSNAP',        45),
    ('USEDDS',          46),
    ('USEDCHILD',       47),
    ('USEDREFRESERV',   48),
    ('USERACCOUNTING',  49),
    ('STMF_SHAREINFO',  50),
    ('DEFER_DESTROY',   51),
    ('USERREFS',        52),
    ('LOGBIAS',         53),
    ('UNIQUE',          54),
    ('OBJSETID',        55),
    ('DEDUP',           56),
    ('MLSLABEL',        57),
    ('SYNC',            58),
    ('REFRATIO',        59),
    ('WRITTEN',         60),
    ('CLONES',          61),
    ('LOGICALUSED',     62),
    ('LOGICALREFERENCED', 63),
    ('INCONSISTENT',    64),
    ('SNAPDEV',         65),
    ('ACLTYPE',         66),
    ('SELINUX_CONTEXT', 67),
    ('SELINUX_FSCONTEXT', 68),
    ('SELINUX_DEFCONTEXT', 69),
    ('SELINUX_ROOTCONTEXT', 70),
    ('RELATIME',        71),
    ('NUM_PROPS',   72),
])

zfs_userquota_prop = IntEnum("zfs_userquota_prop", [
    ("USERUSED",        0),
    ("USERQUOTA",       1),
    ("GROUPUSED",       2),
    ("GROUPQUOTA",      3),
    ("NUM_USERQUOTA_PROPS", 4),
])

zfs_get_column = IntEnum("zfs_get_column", [
    ("NONE",            0),
    ("NAME",            1),
    ("PROPERTY",        2),
    ("VALUE",           3),
    ("RECVD",           4),
    ("SOURCE",          5),
])

zpool_prop = IntEnum("zpool_prop", [
    ("NAME",            0),
    ("SIZE",            1),
    ("CAPACITY",        2),
    ("ALTROOT",         3),
    ("HEALTH",          4),
    ("GUID",            5),
    ("VERSION",         6),
    ("BOOTFS",          7),
    ("DELEGATION",      8),
    ("AUTOREPLACE",     9),
    ("CACHEFILE",       10),
    ("FAILUREMODE",     11),
    ("LISTSNAPS",       12),
    ("AUTOEXPAND",      13),
    ("DEDUPDITTO",      14),
    ("DEDUPRATIO",      15),
    ("FREE",            16),
    ("ALLOCATED",       17),
    ("READONLY",        18),
    ("ASHIFT",          19),
    ("COMMENT",         20),
    ("EXPANDSZ",        21),
    ("FREEING",         22),
    ("NUM_PROPS",       23),
])

zpool_status = IntEnum("zpool_status", [
    ('CORRUPT_CACHE',   0),
    ('MISSING_DEV_R',   1),
    ('MISSING_DEV_NR',  2),
    ('CORRUPT_LABEL_R', 3),
    ('CORRUPT_LABEL_NR', 4),
    ('BAD_GUID_SUM',    5),
    ('CORRUPT_POOL',    6),
    ('CORRUPT_DATA',    7),
    ('FAILING_DEV',     8),
    ('VERSION_NEWER',   9),
    ('HOSTID_MISMATCH', 10),
    ('IO_FAILURE_WAIT', 11),
    ('IO_FAILURE_CONTINUE', 12),
    ('BAD_LOG',         13),
    ('ERRATA',          14),
    ('UNSUP_FEAT_READ', 15),
    ('UNSUP_FEAT_WRITE', 16),
    ('FAULTED_DEV_R',   17),
    ('FAULTED_DEV_NR',  18),
    ('VERSION_OLDER',   19),
    ('FEAT_DISABLED',   20),
    ('RESILVERING',     21),
    ('OFFLINE_DEV',     22),
    ('REMOVED_DEV',     23),
    ('OK',              24),

])

zprop_source = IntEnum("zprop_source", [
    ("NONE",            0x01),
    ("DEFAULT",         0x02),
    ("TEMPORARY",       0x04),
    ("LOCAL",           0x08),
    ("INHERITED",       0x10),
    ("RECEIVED",        0x20),
])

ZPROP_SRC_ALL = 0x3f
ZPROP_SOURCE_VAL_RECVD = "$recvd"
ZPROP_N_MORE_ERRORS = "N_MORE_ERRORS"
ZPROP_HAS_RECVD = "$hasrecvd"

zfs_deleg_who_type = IntEnum("zfs_deleg_who_type", [
    ("UNKNOWN",         0),
    ("USER",            ord('u')),
    ("USER_SETS",       ord('U')),
    ("GROUP",           ord('g')),
    ("GROUP_SETS",      ord('G')),
    ("EVERYONE",        ord('e')),
    ("EVERYONE_SETS",   ord('E')),
    ("CREATE",          ord('c')),
    ("CREATE_SETS",     ord('C')),
    ("NAMED_SET",       ord('s')),
    ("NAMED_SET_SETS",  ord('S')),
])

zfs_deleg_inherit = IntEnum("zfs_deleg_inherit", [
    ("NONE",            0),
    ("PERM_LOCAL",      1),
    ("PERM_DESCENDENT", 2),
    ("PERM_LOCALDESCENDENT", 3),
    ("PERM_CREATE",     4),
])

diff_flags = IntEnum("diff_flags", [
    ("PARSEABLE",       0x01),
    ("TIMESTAMP",       0x02),
    ("CLASSIFY",        0x04),
])

vdef_state = IntEnum("vdef_state", [
    ("UNKNOWN",         0),
    ("CLOSED",          1),
    ("OFFLINE",         2),
    ("REMOVED",         3),
    ("CANT_OPEN",       4),
    ("FAULTED",         5),
    ("DEGRADED",        6),
    ("HEALTHY",         7),
])

vdef_aux = IntEnum("vdef_aux", [
    ("NONE",            0),
    ("OPEN_FAILED",     1),
    ("CORRUPT_DATA",    2),
    ("NO_REPLICAS",     3),
    ("BAD_GUID_SUM",    4),
    ("TOO_SMALL",       5),
    ("BAD_LABEL",       6),
    ("VERSION_NEWER",   7),
    ("VERSION_OLDER",   8),
    ("UNSUP_FEAT",      9),
    ("SPARED",          10),
    ("ERR_EXCEEDED",    11),
    ("IO_FAILURE",      12),
    ("BAD_LOG",         13),
    ("EXTERNAL",        14),
    ("SPLIT_POOL",      15),
])

pool_state = IntEnum("pool_state", [
    ("ACTIVE",          0),
    ("EXPORTED",        1),
    ("DESTROYED",       2),
    ("SPARE",           3),
    ("L2CACHE",         4),
    ("UNINITIALIZED",   5),
    ("UNAVAIL",         6),
    ("POTENTIALLY_ACTIVE", 7),
])

zpool_errata = IntEnum("zpool_errata", [
    ("NONE",            0),
    ("ZOL_2094_SCRUB",  1),
    ("ZOL_2094_ASYNC_DESTROY", 2)
])

zfs_canmount_type = IntEnum("zfs_canmount_type", [
    ("OFF",             0),
    ("ON",              1),
    ("NOAUTO",          2),
])

zfs_logbias_op = IntEnum("zfs_logbias_op", [
    ("LATENCY",         0),
    ("THROUGHPUT",      1),
])

zfs_share_op = IntEnum("zfs_share_op", [
    ("SHARE_NFS",       0),
    ("UNSHARE_NFS",     1),
    ("SHARE_SMB",       2),
    ("UNSHARE_SMB",     3),
])

zfs_smb_acl_op = IntEnum("zfs_smb_acl_op", [
    ("ADD",             0),
    ("REMOVE",          1),
    ("RENAME",          2),
    ("PURGE",           3),
])

zfs_cache_type = IntEnum("zfs_cache_type", [
    ("NONE",            0),
    ("METADATA",        1),
    ("ALL",             2),
])

zfs_sync_type = IntEnum("zfs_sync_type", [
    ("STANDARD",        0),
    ("ALWAYS",          1),
    ("DISABLED",        2),
])

zfs_xattr_type = IntEnum("zfs_xattr_type", [
    ("OFF",             0),
    ("DIR",             1),
    ("SA",              2),
])

pool_scan_func = IntEnum("pool_scan_func", [
    ("NONE",            0),
    ("SCRUB",           1),
    ("RESILVER",        2),
    ("FUNCS",           3),
])

dsl_scan_state = IntEnum("dsl_scan_state", [
    ("NONE",            0),
    ("SCANNING",        1),
    ("FINISHED",        2),
    ("CANCELED",        3),
    ("NUM_STATES",      4),
])

ZPOOL_CONFIG_VERSION = "version"
ZPOOL_CONFIG_POOL_NAME = "name"
ZPOOL_CONFIG_POOL_STATE = "state"
ZPOOL_CONFIG_POOL_TXG = "txg"
ZPOOL_CONFIG_POOL_GUID = "pool_guid"
ZPOOL_CONFIG_CREATE_TXG = "create_txg"
ZPOOL_CONFIG_TOP_GUID = "top_guid"
ZPOOL_CONFIG_VDEV_TREE = "vdev_tree"
ZPOOL_CONFIG_TYPE = "type"
ZPOOL_CONFIG_CHILDREN = "children"
ZPOOL_CONFIG_ID = "id"
ZPOOL_CONFIG_GUID = "guid"
ZPOOL_CONFIG_PATH = "path"
ZPOOL_CONFIG_DEVID = "devid"
ZPOOL_CONFIG_METASLAB_ARRAY = "metaslab_array"
ZPOOL_CONFIG_METASLAB_SHIFT = "metaslab_shift"
ZPOOL_CONFIG_ASHIFT = "ashift"
ZPOOL_CONFIG_ASIZE = "asize"
ZPOOL_CONFIG_DTL = "DTL"
ZPOOL_CONFIG_SCAN_STATS = "scan_stats"  # not stored on disk
ZPOOL_CONFIG_VDEV_STATS = "vdev_stats"  # not stored on disk
ZPOOL_CONFIG_WHOLE_DISK = "whole_disk"
ZPOOL_CONFIG_ERRCOUNT = "error_count"
ZPOOL_CONFIG_NOT_PRESENT = "not_present"
ZPOOL_CONFIG_SPARES = "spares"
ZPOOL_CONFIG_IS_SPARE = "is_spare"
ZPOOL_CONFIG_NPARITY = "nparity"
ZPOOL_CONFIG_HOSTID = "hostid"
ZPOOL_CONFIG_HOSTNAME = "hostname"
ZPOOL_CONFIG_LOADED_TIME = "initial_load_time"
ZPOOL_CONFIG_UNSPARE = "unspare"
ZPOOL_CONFIG_PHYS_PATH = "phys_path"
ZPOOL_CONFIG_IS_LOG = "is_log"
ZPOOL_CONFIG_L2CACHE = "l2cache"
ZPOOL_CONFIG_HOLE_ARRAY = "hole_array"
ZPOOL_CONFIG_VDEV_CHILDREN = "vdev_children"
ZPOOL_CONFIG_IS_HOLE = "is_hole"
ZPOOL_CONFIG_DDT_HISTOGRAM = "ddt_histogram"
ZPOOL_CONFIG_DDT_OBJ_STATS = "ddt_object_stats"
ZPOOL_CONFIG_DDT_STATS = "ddt_stats"
ZPOOL_CONFIG_SPLIT = "splitcfg"
ZPOOL_CONFIG_ORIG_GUID = "orig_guid"
ZPOOL_CONFIG_SPLIT_GUID = "split_guid"
ZPOOL_CONFIG_SPLIT_LIST = "guid_list"
ZPOOL_CONFIG_REMOVING = "removing"
ZPOOL_CONFIG_RESILVER_TXG = "resilver_txg"
ZPOOL_CONFIG_COMMENT = "comment"
ZPOOL_CONFIG_SUSPENDED = "suspended"  # not stored on disk
ZPOOL_CONFIG_TIMESTAMP = "timestamp"  # not stored on disk
ZPOOL_CONFIG_BOOTFS = "bootfs"  # not stored on disk
ZPOOL_CONFIG_MISSING_DEVICES = "missing_vdevs"  # not stored on disk
ZPOOL_CONFIG_LOAD_INFO = "load_info"  # not stored on disk
ZPOOL_CONFIG_REWIND_INFO = "rewind_info"  # not stored on disk
ZPOOL_CONFIG_UNSUP_FEAT = "unsup_feat"  # not stored on disk
ZPOOL_CONFIG_ENABLED_FEAT = "enabled_feat"  # not stored on disk
ZPOOL_CONFIG_CAN_RDONLY = "can_rdonly"  # not stored on disk
ZPOOL_CONFIG_FEATURES_FOR_READ = "features_for_read"
ZPOOL_CONFIG_FEATURE_STATS = "feature_stats"  # not stored on disk
ZPOOL_CONFIG_ERRATA = "errata"  # not stored on disk

ZPOOL_CONFIG_OFFLINE = "offline"
ZPOOL_CONFIG_FAULTED = "faulted"
ZPOOL_CONFIG_DEGRADED = "degraded"
ZPOOL_CONFIG_REMOVED = "removed"
ZPOOL_CONFIG_FRI = "fru"
ZPOOL_CONFIG_AUX_STATE = "aux_state"

VDEV_TYPE_ROOT = "root"
VDEV_TYPE_MIRROR = "mirror"
VDEV_TYPE_REPLACING = "replacing"
VDEV_TYPE_RAIDZ = "raidz"
VDEV_TYPE_DISK = "disk"
VDEV_TYPE_FILE = "file"
VDEV_TYPE_MISSING = "missing"
VDEV_TYPE_HOLE = "hole"
VDEV_TYPE_SPARE = "spare"
VDEV_TYPE_LOG = "log"
VDEV_TYPE_L2CACHE = "l2cache"


MAXNAMELEN = 256
ZFS_MAXNAMELEN = MAXNAMELEN
ZPOOL_MAXNAMELEN = MAXNAMELEN
