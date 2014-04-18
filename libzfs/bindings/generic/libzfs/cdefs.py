from collections import OrderedDict

TYPEDEFS = OrderedDict([
    ('zfs_error_t', """
typedef enum zfs_error {
    EZFS_SUCCESS = 0,   /* no error -- success */
    EZFS_NOMEM = 2000,  /* out of memory */
    EZFS_BADPROP,       /* invalid property value */
    EZFS_PROPREADONLY,  /* cannot set readonly property */
    EZFS_PROPTYPE,      /* property does not apply to dataset type */
    EZFS_PROPNONINHERIT,    /* property is not inheritable */
    EZFS_PROPSPACE,     /* bad quota or reservation */
    EZFS_BADTYPE,       /* dataset is not of appropriate type */
    EZFS_BUSY,      /* pool or dataset is busy */
    EZFS_EXISTS,        /* pool or dataset already exists */
    EZFS_NOENT,     /* no such pool or dataset */
    EZFS_BADSTREAM,     /* bad backup stream */
    EZFS_DSREADONLY,    /* dataset is readonly */
    EZFS_VOLTOOBIG,     /* volume is too large for 32-bit system */
    EZFS_INVALIDNAME,   /* invalid dataset name */
    EZFS_BADRESTORE,    /* unable to restore to destination */
    EZFS_BADBACKUP,     /* backup failed */
    EZFS_BADTARGET,     /* bad attach/detach/replace target */
    EZFS_NODEVICE,      /* no such device in pool */
    EZFS_BADDEV,        /* invalid device to add */
    EZFS_NOREPLICAS,    /* no valid replicas */
    EZFS_RESILVERING,   /* currently resilvering */
    EZFS_BADVERSION,    /* unsupported version */
    EZFS_POOLUNAVAIL,   /* pool is currently unavailable */
    EZFS_DEVOVERFLOW,   /* too many devices in one vdev */
    EZFS_BADPATH,       /* must be an absolute path */
    EZFS_CROSSTARGET,   /* rename or clone across pool or dataset */
    EZFS_ZONED,     /* used improperly in local zone */
    EZFS_MOUNTFAILED,   /* failed to mount dataset */
    EZFS_UMOUNTFAILED,  /* failed to unmount dataset */
    EZFS_UNSHARENFSFAILED,  /* unshare(1M) failed */
    EZFS_SHARENFSFAILED,    /* share(1M) failed */
    EZFS_PERM,      /* permission denied */
    EZFS_NOSPC,     /* out of space */
    EZFS_FAULT,     /* bad address */
    EZFS_IO,        /* I/O error */
    EZFS_INTR,      /* signal received */
    EZFS_ISSPARE,       /* device is a hot spare */
    EZFS_INVALCONFIG,   /* invalid vdev configuration */
    EZFS_RECURSIVE,     /* recursive dependency */
    EZFS_NOHISTORY,     /* no history object */
    EZFS_POOLPROPS,     /* couldn't retrieve pool props */
    EZFS_POOL_NOTSUP,   /* ops not supported for this type of pool */
    EZFS_POOL_INVALARG, /* invalid argument for this pool operation */
    EZFS_NAMETOOLONG,   /* dataset name is too long */
    EZFS_OPENFAILED,    /* open of device failed */
    EZFS_NOCAP,     /* couldn't get capacity */
    EZFS_LABELFAILED,   /* write of label failed */
    EZFS_BADWHO,        /* invalid permission who */
    EZFS_BADPERM,       /* invalid permission */
    EZFS_BADPERMSET,    /* invalid permission set name */
    EZFS_NODELEGATION,  /* delegated administration is disabled */
    EZFS_UNSHARESMBFAILED,  /* failed to unshare over smb */
    EZFS_SHARESMBFAILED,    /* failed to share over smb */
    EZFS_BADCACHE,      /* bad cache file */
    EZFS_ISL2CACHE,     /* device is for the level 2 ARC */
    EZFS_VDEVNOTSUP,    /* unsupported vdev type */
    EZFS_NOTSUP,        /* ops not supported on this dataset */
    EZFS_ACTIVE_SPARE,  /* pool has active shared spare devices */
    EZFS_UNPLAYED_LOGS, /* log device has unplayed logs */
    EZFS_REFTAG_RELE,   /* snapshot release: tag not found */
    EZFS_REFTAG_HOLD,   /* snapshot hold: tag already exists */
    EZFS_TAGTOOLONG,    /* snapshot hold/rele: tag too long */
    EZFS_PIPEFAILED,    /* pipe create failed */
    EZFS_THREADCREATEFAILED, /* thread create failed */
    EZFS_POSTSPLIT_ONLINE,  /* onlining a disk after splitting it */
    EZFS_SCRUBBING,     /* currently scrubbing */
    EZFS_NO_SCRUB,      /* no active scrub */
    EZFS_DIFF,      /* general failure of zfs diff */
    EZFS_DIFFDATA,      /* bad zfs diff data */
    EZFS_POOLREADONLY,  /* pool is in read-only mode */
    EZFS_UNKNOWN
} zfs_error_t;
"""),
    ('zfs_type_t', """
typedef enum {
    ZFS_TYPE_FILESYSTEM = 0x1,
    ZFS_TYPE_SNAPSHOT   = 0x2,
    ZFS_TYPE_VOLUME     = 0x4,
    ZFS_TYPE_POOL       = 0x8
} zfs_type_t;
"""),
    ('zfs_prop_t', """
typedef enum {
    ZFS_PROP_TYPE,
    ZFS_PROP_CREATION,
    ZFS_PROP_USED,
    ZFS_PROP_AVAILABLE,
    ZFS_PROP_REFERENCED,
    ZFS_PROP_COMPRESSRATIO,
    ZFS_PROP_MOUNTED,
    ZFS_PROP_ORIGIN,
    ZFS_PROP_QUOTA,
    ZFS_PROP_RESERVATION,
    ZFS_PROP_VOLSIZE,
    ZFS_PROP_VOLBLOCKSIZE,
    ZFS_PROP_RECORDSIZE,
    ZFS_PROP_MOUNTPOINT,
    ZFS_PROP_SHARENFS,
    ZFS_PROP_CHECKSUM,
    ZFS_PROP_COMPRESSION,
    ZFS_PROP_ATIME,
    ZFS_PROP_DEVICES,
    ZFS_PROP_EXEC,
    ZFS_PROP_SETUID,
    ZFS_PROP_READONLY,
    ZFS_PROP_ZONED,
    ZFS_PROP_SNAPDIR,
    ZFS_PROP_PRIVATE,       /* not exposed to user, temporary */
    ZFS_PROP_ACLINHERIT,
    ZFS_PROP_CREATETXG,     /* not exposed to the user */
    ZFS_PROP_NAME,          /* not exposed to the user */
    ZFS_PROP_CANMOUNT,
    ZFS_PROP_ISCSIOPTIONS,      /* not exposed to the user */
    ZFS_PROP_XATTR,
    ZFS_PROP_NUMCLONES,     /* not exposed to the user */
    ZFS_PROP_COPIES,
    ZFS_PROP_VERSION,
    ZFS_PROP_UTF8ONLY,
    ZFS_PROP_NORMALIZE,
    ZFS_PROP_CASE,
    ZFS_PROP_VSCAN,
    ZFS_PROP_NBMAND,
    ZFS_PROP_SHARESMB,
    ZFS_PROP_REFQUOTA,
    ZFS_PROP_REFRESERVATION,
    ZFS_PROP_GUID,
    ZFS_PROP_PRIMARYCACHE,
    ZFS_PROP_SECONDARYCACHE,
    ZFS_PROP_USEDSNAP,
    ZFS_PROP_USEDDS,
    ZFS_PROP_USEDCHILD,
    ZFS_PROP_USEDREFRESERV,
    ZFS_PROP_USERACCOUNTING,    /* not exposed to the user */
    ZFS_PROP_STMF_SHAREINFO,    /* not exposed to the user */
    ZFS_PROP_DEFER_DESTROY,
    ZFS_PROP_USERREFS,
    ZFS_PROP_LOGBIAS,
    ZFS_PROP_UNIQUE,        /* not exposed to the user */
    ZFS_PROP_OBJSETID,      /* not exposed to the user */
    ZFS_PROP_DEDUP,
    ZFS_PROP_MLSLABEL,
    ZFS_PROP_SYNC,
    ZFS_PROP_REFRATIO,
    ZFS_PROP_WRITTEN,
    ZFS_PROP_CLONES,
    ZFS_PROP_LOGICALUSED,
    ZFS_PROP_LOGICALREFERENCED,
    ZFS_PROP_INCONSISTENT,      /* not exposed to the user */
    ZFS_PROP_SNAPDEV,
    ZFS_PROP_ACLTYPE,
    ZFS_PROP_SELINUX_CONTEXT,
    ZFS_PROP_SELINUX_FSCONTEXT,
    ZFS_PROP_SELINUX_DEFCONTEXT,
    ZFS_PROP_SELINUX_ROOTCONTEXT,
    ZFS_PROP_RELATIME,
    ZFS_NUM_PROPS
} zfs_prop_t;
"""),
    ('zfs_userquota_prop_t', """
typedef enum {
    ZFS_PROP_USERUSED,
    ZFS_PROP_USERQUOTA,
    ZFS_PROP_GROUPUSED,
    ZFS_PROP_GROUPQUOTA,
    ZFS_NUM_USERQUOTA_PROPS
} zfs_userquota_prop_t;
"""),
    ('zpool_prop_t', """
typedef enum {
    ZPOOL_PROP_NAME,
    ZPOOL_PROP_SIZE,
    ZPOOL_PROP_CAPACITY,
    ZPOOL_PROP_ALTROOT,
    ZPOOL_PROP_HEALTH,
    ZPOOL_PROP_GUID,
    ZPOOL_PROP_VERSION,
    ZPOOL_PROP_BOOTFS,
    ZPOOL_PROP_DELEGATION,
    ZPOOL_PROP_AUTOREPLACE,
    ZPOOL_PROP_CACHEFILE,
    ZPOOL_PROP_FAILUREMODE,
    ZPOOL_PROP_LISTSNAPS,
    ZPOOL_PROP_AUTOEXPAND,
    ZPOOL_PROP_DEDUPDITTO,
    ZPOOL_PROP_DEDUPRATIO,
    ZPOOL_PROP_FREE,
    ZPOOL_PROP_ALLOCATED,
    ZPOOL_PROP_READONLY,
    ZPOOL_PROP_ASHIFT,
    ZPOOL_PROP_COMMENT,
    ZPOOL_PROP_EXPANDSZ,
    ZPOOL_PROP_FREEING,
    ZPOOL_NUM_PROPS
} zpool_prop_t;
"""),
    ('zprop_source_t', """
typedef enum {
    ZPROP_SRC_NONE = 0x1,
    ZPROP_SRC_DEFAULT = 0x2,
    ZPROP_SRC_TEMPORARY = 0x4,
    ZPROP_SRC_LOCAL = 0x8,
    ZPROP_SRC_INHERITED = 0x10,
    ZPROP_SRC_RECEIVED = 0x20
} zprop_source_t;
"""),
    ('zfs_deleg_who_type_t', """
typedef enum {
    ZFS_DELEG_WHO_UNKNOWN = 0,
    ZFS_DELEG_USER = 117,
    ZFS_DELEG_USER_SETS = 85,
    ZFS_DELEG_GROUP = 103,
    ZFS_DELEG_GROUP_SETS = 71,
    ZFS_DELEG_EVERYONE = 101,
    ZFS_DELEG_EVERYONE_SETS = 69,
    ZFS_DELEG_CREATE = 99,
    ZFS_DELEG_CREATE_SETS = 67,
    ZFS_DELEG_NAMED_SET = 115,
    ZFS_DELEG_NAMED_SET_SETS = 83
} zfs_deleg_who_type_t;
"""),
    ('zfs_deleg_inherit_t', """
typedef enum {
    ZFS_DELEG_NONE = 0,
    ZFS_DELEG_PERM_LOCAL = 1,
    ZFS_DELEG_PERM_DESCENDENT = 2,
    ZFS_DELEG_PERM_LOCALDESCENDENT = 3,
    ZFS_DELEG_PERM_CREATE = 4
} zfs_deleg_inherit_t;
""")
])

FUNCTIONS = OrderedDict()
