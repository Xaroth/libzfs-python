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
    ('zpool_status_t', """
typedef enum {
    /*
     * The following correspond to faults as defined in the (fault.fs.zfs.*)
     * event namespace.  Each is associated with a corresponding message ID.
     */
    ZPOOL_STATUS_CORRUPT_CACHE, /* corrupt /kernel/drv/zpool.cache */
    ZPOOL_STATUS_MISSING_DEV_R, /* missing device with replicas */
    ZPOOL_STATUS_MISSING_DEV_NR,    /* missing device with no replicas */
    ZPOOL_STATUS_CORRUPT_LABEL_R,   /* bad device label with replicas */
    ZPOOL_STATUS_CORRUPT_LABEL_NR,  /* bad device label with no replicas */
    ZPOOL_STATUS_BAD_GUID_SUM,  /* sum of device guids didn't match */
    ZPOOL_STATUS_CORRUPT_POOL,  /* pool metadata is corrupted */
    ZPOOL_STATUS_CORRUPT_DATA,  /* data errors in user (meta)data */
    ZPOOL_STATUS_FAILING_DEV,   /* device experiencing errors */
    ZPOOL_STATUS_VERSION_NEWER, /* newer on-disk version */
    ZPOOL_STATUS_HOSTID_MISMATCH,   /* last accessed by another system */
    ZPOOL_STATUS_IO_FAILURE_WAIT,   /* failed I/O, failmode 'wait' */
    ZPOOL_STATUS_IO_FAILURE_CONTINUE, /* failed I/O, failmode 'continue' */
    ZPOOL_STATUS_BAD_LOG,       /* cannot read log chain(s) */
    ZPOOL_STATUS_ERRATA,        /* informational errata available */

    /*
     * If the pool has unsupported features but can still be opened in
     * read-only mode, its status is ZPOOL_STATUS_UNSUP_FEAT_WRITE. If the
     * pool has unsupported features but cannot be opened at all, its
     * status is ZPOOL_STATUS_UNSUP_FEAT_READ.
     */
    ZPOOL_STATUS_UNSUP_FEAT_READ,   /* unsupported features for read */
    ZPOOL_STATUS_UNSUP_FEAT_WRITE,  /* unsupported features for write */

    /*
     * These faults have no corresponding message ID.  At the time we are
     * checking the status, the original reason for the FMA fault (I/O or
     * checksum errors) has been lost.
     */
    ZPOOL_STATUS_FAULTED_DEV_R, /* faulted device with replicas */
    ZPOOL_STATUS_FAULTED_DEV_NR,    /* faulted device with no replicas */

    /*
     * The following are not faults per se, but still an error possibly
     * requiring administrative attention.  There is no corresponding
     * message ID.
     */
    ZPOOL_STATUS_VERSION_OLDER, /* older legacy on-disk version */
    ZPOOL_STATUS_FEAT_DISABLED, /* supported features are disabled */
    ZPOOL_STATUS_RESILVERING,   /* device being resilvered */
    ZPOOL_STATUS_OFFLINE_DEV,   /* device online */
    ZPOOL_STATUS_REMOVED_DEV,   /* removed device */

    /*
     * Finally, the following indicates a healthy pool.
     */
    ZPOOL_STATUS_OK
} zpool_status_t;
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
"""),
    ('zfs_handle_t', """
typedef struct zfs_handle zfs_handle_t;
"""),
    ('zpool_handle_t', """
typedef struct zpool_handle zpool_handle_t;
"""),
    ('libzfs_handle_t', """
typedef struct libzfs_handle libzfs_handle_t;
"""),
    ('zfs_get_column_t', """
typedef enum {
    GET_COL_NONE,
    GET_COL_NAME,
    GET_COL_PROPERTY,
    GET_COL_VALUE,
    GET_COL_RECVD,
    GET_COL_SOURCE
} zfs_get_column_t;
"""),
    ('sendflags_t', """
typedef struct sendflags {
    /* print informational messages (ie, -v was specified) */
    boolean_t verbose;

    /* recursive send  (ie, -R) */
    boolean_t replicate;

    /* for incrementals, do all intermediate snapshots */
    boolean_t doall;

    /* if dataset is a clone, do incremental from its origin */
    boolean_t fromorigin;

    /* do deduplication */
    boolean_t dedup;

    /* send properties (ie, -p) */
    boolean_t props;

    /* do not send (no-op, ie. -n) */
    boolean_t dryrun;

    /* parsable verbose output (ie. -P) */
    boolean_t parsable;

    /* show progress (ie. -v) */
    boolean_t progress;
} sendflags_t;
"""),
    ('recvflags_t', """
typedef struct recvflags {
    /* print informational messages (ie, -v was specified) */
    boolean_t verbose;

    /* the destination is a prefix, not the exact fs (ie, -d) */
    boolean_t isprefix;

    /*
     * Only the tail of the sent snapshot path is appended to the
     * destination to determine the received snapshot name (ie, -e).
     */
    boolean_t istail;

    /* do not actually do the recv, just check if it would work (ie, -n) */
    boolean_t dryrun;

    /* rollback/destroy filesystems as necessary (eg, -F) */
    boolean_t force;

    /* set "canmount=off" on all modified filesystems */
    boolean_t canmountoff;

    /* byteswap flag is used internally; callers need not specify */
    boolean_t byteswap;

    /* do not mount file systems as they are extracted (private) */
    boolean_t nomount;
} recvflags_t;
"""),
    ('diff_flags_t', """
typedef enum diff_flags {
    ZFS_DIFF_PARSEABLE = 0x1,
    ZFS_DIFF_TIMESTAMP = 0x2,
    ZFS_DIFF_CLASSIFY = 0x4
} diff_flags_t;
"""),
    ('snapfilter_cb_t', """
typedef boolean_t (snapfilter_cb_t)(zfs_handle_t *, void *);
"""),
    #('zfs_userspace_cb_t', """
    #    typedef int (*zfs_userspace_cb_t)(void *arg, const char *domain, uid_t rid, uint64_t space);
    #"""),
    ('zpool_iter_f', """
typedef int (*zpool_iter_f)(zpool_handle_t *, void *);
"""),
    ('zfs_iter_f', """
typedef int (*zfs_iter_f)(zfs_handle_t *, void *);
"""),
    ('zprop_func', """
typedef int (*zprop_func)(int, void *);
"""),
    ('vdef_state_t', """
typedef enum vdev_state {
    VDEV_STATE_UNKNOWN = 0, /* Uninitialized vdev           */
    VDEV_STATE_CLOSED,  /* Not currently open           */
    VDEV_STATE_OFFLINE, /* Not allowed to open          */
    VDEV_STATE_REMOVED, /* Explicitly removed from system   */
    VDEV_STATE_CANT_OPEN,   /* Tried to open, but failed        */
    VDEV_STATE_FAULTED, /* External request to fault device */
    VDEV_STATE_DEGRADED,    /* Replicated vdev with unhealthy kids  */
    VDEV_STATE_HEALTHY  /* Presumed good            */
} vdev_state_t;
"""),
    ('vdef_aux_t', """
typedef enum vdev_aux {
    VDEV_AUX_NONE,      /* no error             */
    VDEV_AUX_OPEN_FAILED,   /* ldi_open_*() or vn_open() failed */
    VDEV_AUX_CORRUPT_DATA,  /* bad label or disk contents       */
    VDEV_AUX_NO_REPLICAS,   /* insufficient number of replicas  */
    VDEV_AUX_BAD_GUID_SUM,  /* vdev guid sum doesn't match      */
    VDEV_AUX_TOO_SMALL, /* vdev size is too small       */
    VDEV_AUX_BAD_LABEL, /* the label is OK but invalid      */
    VDEV_AUX_VERSION_NEWER, /* on-disk version is too new       */
    VDEV_AUX_VERSION_OLDER, /* on-disk version is too old       */
    VDEV_AUX_UNSUP_FEAT,    /* unsupported features         */
    VDEV_AUX_SPARED,    /* hot spare used in another pool   */
    VDEV_AUX_ERR_EXCEEDED,  /* too many errors          */
    VDEV_AUX_IO_FAILURE,    /* experienced I/O failure      */
    VDEV_AUX_BAD_LOG,   /* cannot read log chain(s)     */
    VDEV_AUX_EXTERNAL,  /* external diagnosis           */
    VDEV_AUX_SPLIT_POOL /* vdev was split off into another pool */
} vdev_aux_t;
"""),
    ('pool_state_t', """
typedef enum pool_state {
    POOL_STATE_ACTIVE = 0,      /* In active use        */
    POOL_STATE_EXPORTED,        /* Explicitly exported      */
    POOL_STATE_DESTROYED,       /* Explicitly destroyed     */
    POOL_STATE_SPARE,       /* Reserved for hot spare use   */
    POOL_STATE_L2CACHE,     /* Level 2 ARC device       */
    POOL_STATE_UNINITIALIZED,   /* Internal spa_t state     */
    POOL_STATE_UNAVAIL,     /* Internal libzfs state    */
    POOL_STATE_POTENTIALLY_ACTIVE   /* Internal libzfs state    */
} pool_state_t;
"""),
    ('zpool_errata_t', """
typedef enum zpool_errata {
    ZPOOL_ERRATA_NONE,
    ZPOOL_ERRATA_ZOL_2094_SCRUB,
    ZPOOL_ERRATA_ZOL_2094_ASYNC_DESTROY,
} zpool_errata_t;
"""),
    ('zprop_list_t', """
typedef struct zprop_list {
    int     pl_prop;
    char        *pl_user_prop;
    struct zprop_list *pl_next;
    boolean_t   pl_all;
    size_t      pl_width;
    size_t      pl_recvd_width;
    boolean_t   pl_fixed;
} zprop_list_t;
"""),
    ('zfs_canmount_type_t', """
typedef enum {
    ZFS_CANMOUNT_OFF = 0,
    ZFS_CANMOUNT_ON = 1,
    ZFS_CANMOUNT_NOAUTO = 2
} zfs_canmount_type_t;
"""),
    ('zfs_logbias_op_t', """
typedef enum {
    ZFS_LOGBIAS_LATENCY = 0,
    ZFS_LOGBIAS_THROUGHPUT = 1
} zfs_logbias_op_t;
"""),
    ('zfs_share_op_t', """
typedef enum zfs_share_op {
    ZFS_SHARE_NFS = 0,
    ZFS_UNSHARE_NFS = 1,
    ZFS_SHARE_SMB = 2,
    ZFS_UNSHARE_SMB = 3
} zfs_share_op_t;
"""),
    ('zfs_smb_acl_op_t', """
typedef enum zfs_smb_acl_op {
    ZFS_SMB_ACL_ADD,
    ZFS_SMB_ACL_REMOVE,
    ZFS_SMB_ACL_RENAME,
    ZFS_SMB_ACL_PURGE
} zfs_smb_acl_op_t;
"""),
    ('zfs_cache_type_t', """
typedef enum zfs_cache_type {
    ZFS_CACHE_NONE = 0,
    ZFS_CACHE_METADATA = 1,
    ZFS_CACHE_ALL = 2
} zfs_cache_type_t;
"""),
    ('zfs_sync_type_t', """
typedef enum {
    ZFS_SYNC_STANDARD = 0,
    ZFS_SYNC_ALWAYS = 1,
    ZFS_SYNC_DISABLED = 2
} zfs_sync_type_t;
"""),
    ('zfs_xattr_type_t', """
typedef enum {
    ZFS_XATTR_OFF = 0,
    ZFS_XATTR_DIR = 1,
    ZFS_XATTR_SA = 2
} zfs_xattr_type_t;
"""),
    ('pool_scan_func_t', """
typedef enum pool_scan_func {
    POOL_SCAN_NONE,
    POOL_SCAN_SCRUB,
    POOL_SCAN_RESILVER,
    POOL_SCAN_FUNCS
} pool_scan_func_t;
"""),
    ('splitflags_t', """
typedef struct splitflags {
    /* do not split, but return the config that would be split off */
    int dryrun : 1;

    /* after splitting, import the pool */
    int import : 1;
} splitflags_t;
"""),
    ('importargs_t', """
typedef struct importargs {
    char **path;        /* a list of paths to search        */
    int paths;      /* number of paths to search        */
    char *poolname;     /* name of a pool to find       */
    uint64_t guid;      /* guid of a pool to find       */
    char *cachefile;    /* cachefile to use for import      */
    int can_be_active : 1;  /* can the pool be active?      */
    int unique : 1;     /* does 'poolname' already exist?   */
    int exists : 1;     /* set on return if pool already exists */
} importargs_t;
"""),
])

FUNCTIONS = OrderedDict([
    ('libzfs_init', 'libzfs_handle_t *libzfs_init(void);'),
    ('libzfs_fini', 'void libzfs_fini(libzfs_handle_t *);'),
    ('zpool_get_handle', 'libzfs_handle_t *zpool_get_handle(zpool_handle_t *);'),
    ('zfs_get_handle', 'libzfs_handle_t *zfs_get_handle(zfs_handle_t *);'),
    ('libzfs_print_on_error', 'void libzfs_print_on_error(libzfs_handle_t *, boolean_t);'),
    ('zfs_save_arguments', 'void zfs_save_arguments(int argc, char **, char *, int);'),
    ('zpool_log_history', 'int zpool_log_history(libzfs_handle_t *, const char *);'),
    ('libzfs_errno', 'int libzfs_errno(libzfs_handle_t *);'),
    ('libzfs_error_action', 'const char *libzfs_error_action(libzfs_handle_t *);'),
    ('libzfs_error_description', 'const char *libzfs_error_description(libzfs_handle_t *);'),
    ('libzfs_mnttab_init', 'void libzfs_mnttab_init(libzfs_handle_t *);'),
    ('libzfs_mnttab_fini', 'void libzfs_mnttab_fini(libzfs_handle_t *);'),
    ('libzfs_mnttab_cache', 'void libzfs_mnttab_cache(libzfs_handle_t *, boolean_t);'),
    ('libzfs_mnttab_find', 'int libzfs_mnttab_find(libzfs_handle_t *, const char *, struct mnttab *);'),
    ('libzfs_mnttab_add', 'void libzfs_mnttab_add(libzfs_handle_t *, const char *, const char *, const char *);'),
    ('libzfs_mnttab_remove', 'void libzfs_mnttab_remove(libzfs_handle_t *, const char *);'),
    ('zpool_open', 'zpool_handle_t *zpool_open(libzfs_handle_t *, const char *);'),
    ('zpool_open_canfail', 'zpool_handle_t *zpool_open_canfail(libzfs_handle_t *, const char *);'),
    ('zpool_close', 'void zpool_close(zpool_handle_t *);'),
    ('zpool_get_name', 'const char *zpool_get_name(zpool_handle_t *);'),
    ('zpool_get_state', 'int zpool_get_state(zpool_handle_t *);'),
    ('zpool_state_to_name', 'char *zpool_state_to_name(vdev_state_t, vdev_aux_t);'),
    ('zpool_pool_state_to_name', 'const char *zpool_pool_state_to_name(pool_state_t);'),
    ('zpool_free_handles', 'void zpool_free_handles(libzfs_handle_t *);'),
    ('zpool_iter', 'int zpool_iter(libzfs_handle_t *, zpool_iter_f, void *);'),
    ('zpool_create', 'int zpool_create(libzfs_handle_t *, const char *, nvlist_t *, nvlist_t *, nvlist_t *);'),
    ('zpool_destroy', 'int zpool_destroy(zpool_handle_t *, const char *);'),
    ('zpool_add', 'int zpool_add(zpool_handle_t *, nvlist_t *);'),
    ('zpool_scan', 'int zpool_scan(zpool_handle_t *, pool_scan_func_t);'),
    ('zpool_clear', 'int zpool_clear(zpool_handle_t *, const char *, nvlist_t *);'),
    ('zpool_reguid', 'int zpool_reguid(zpool_handle_t *);'),
    ('zpool_reopen', 'int zpool_reopen(zpool_handle_t *);'),
    ('zpool_vdev_online', 'int zpool_vdev_online(zpool_handle_t *, const char *, int, vdev_state_t *);'),
    ('zpool_vdev_offline', 'int zpool_vdev_offline(zpool_handle_t *, const char *, boolean_t);'),
    ('zpool_vdev_attach', 'int zpool_vdev_attach(zpool_handle_t *, const char *, const char *, nvlist_t *, int);'),
    ('zpool_vdev_detach', 'int zpool_vdev_detach(zpool_handle_t *, const char *);'),
    ('zpool_vdev_remove', 'int zpool_vdev_remove(zpool_handle_t *, const char *);'),
    ('zpool_vdev_split', 'int zpool_vdev_split(zpool_handle_t *, char *, nvlist_t **, nvlist_t *, splitflags_t);'),
    ('zpool_vdev_fault', 'int zpool_vdev_fault(zpool_handle_t *, uint64_t, vdev_aux_t);'),
    ('zpool_vdev_degrade', 'int zpool_vdev_degrade(zpool_handle_t *, uint64_t, vdev_aux_t);'),
    ('zpool_vdev_clear', 'int zpool_vdev_clear(zpool_handle_t *, uint64_t);'),
    ('zpool_find_vdev', 'nvlist_t *zpool_find_vdev(zpool_handle_t *, const char *, boolean_t *, boolean_t *, boolean_t *);'),
    ('zpool_find_vdev_by_physpath', 'nvlist_t *zpool_find_vdev_by_physpath(zpool_handle_t *, const char *, boolean_t *, boolean_t *, boolean_t *);'),
    ('zpool_label_disk_wait', 'int zpool_label_disk_wait(char *, int);'),
    ('zpool_label_disk', 'int zpool_label_disk(libzfs_handle_t *, zpool_handle_t *, char *);'),
    ('zpool_set_prop', 'int zpool_set_prop(zpool_handle_t *, const char *, const char *);'),
    ('zpool_get_prop', 'int zpool_get_prop(zpool_handle_t *, zpool_prop_t, char *, size_t proplen, zprop_source_t *);'),
    ('zpool_get_prop_literal', 'int zpool_get_prop_literal(zpool_handle_t *, zpool_prop_t, char *, size_t proplen, zprop_source_t *, boolean_t literal);'),
    ('zpool_get_prop_int', 'uint64_t zpool_get_prop_int(zpool_handle_t *, zpool_prop_t, zprop_source_t *);'),
    ('zpool_prop_to_name', 'const char *zpool_prop_to_name(zpool_prop_t);'),
    ('zpool_prop_values', 'const char *zpool_prop_values(zpool_prop_t);'),
    ('zpool_get_status', 'zpool_status_t zpool_get_status(zpool_handle_t *, char **, zpool_errata_t *);'),
    ('zpool_import_status', 'zpool_status_t zpool_import_status(nvlist_t *, char **, zpool_errata_t *);'),
    #('zpool_dump_ddt', 'void zpool_dump_ddt(const ddt_stat_t *dds, const ddt_histogram_t *ddh);'),  # TODO: ddt_histogram_t
    ('zpool_get_config', 'nvlist_t *zpool_get_config(zpool_handle_t *, nvlist_t **);'),
    ('zpool_get_features', 'nvlist_t *zpool_get_features(zpool_handle_t *);'),
    ('zpool_refresh_stats', 'int zpool_refresh_stats(zpool_handle_t *, boolean_t *);'),
    ('zpool_get_errlog', 'int zpool_get_errlog(zpool_handle_t *, nvlist_t **);'),
    ('zpool_export', 'int zpool_export(zpool_handle_t *, boolean_t, const char *);'),
    ('zpool_export_force', 'int zpool_export_force(zpool_handle_t *, const char *);'),
    ('zpool_import', 'int zpool_import(libzfs_handle_t *, nvlist_t *, const char *, char *altroot);'),
    ('zpool_import_props', 'int zpool_import_props(libzfs_handle_t *, nvlist_t *, const char *, nvlist_t *, int);'),
    ('zpool_print_unsup_feat', 'void zpool_print_unsup_feat(nvlist_t *config);'),
    ('zpool_search_import', 'nvlist_t *zpool_search_import(libzfs_handle_t *, importargs_t *);'),
    ('zpool_find_import', 'nvlist_t *zpool_find_import(libzfs_handle_t *, int, char **);'),
    ('zpool_find_import_cached', 'nvlist_t *zpool_find_import_cached(libzfs_handle_t *, const char *, char *, uint64_t);'),
    ('zpool_vdev_name', 'char *zpool_vdev_name(libzfs_handle_t *, zpool_handle_t *, nvlist_t *, boolean_t verbose);'),
    ('zpool_upgrade', 'int zpool_upgrade(zpool_handle_t *, uint64_t);'),
    ('zpool_get_history', 'int zpool_get_history(zpool_handle_t *, nvlist_t **);'),
    ('zpool_history_unpack', 'int zpool_history_unpack(char *, uint64_t, uint64_t *, nvlist_t ***, uint_t *);'),
    ('zpool_events_next', 'int zpool_events_next(libzfs_handle_t *, nvlist_t **, int *, unsigned, int);'),
    ('zpool_events_clear', 'int zpool_events_clear(libzfs_handle_t *, int *);'),
    ('zpool_events_seek', 'int zpool_events_seek(libzfs_handle_t *, uint64_t, int);'),
    ('zpool_obj_to_path', 'void zpool_obj_to_path(zpool_handle_t *, uint64_t, uint64_t, char *, size_t len);'),
    ('zfs_ioctl', 'int zfs_ioctl(libzfs_handle_t *, int, struct zfs_cmd *);'),
    ('zpool_get_physpath', 'int zpool_get_physpath(zpool_handle_t *, char *, size_t);'),
    ('zpool_explain_recover', 'void zpool_explain_recover(libzfs_handle_t *, const char *, int, nvlist_t *);'),
    ('zfs_open', 'zfs_handle_t *zfs_open(libzfs_handle_t *, const char *, int);'),
    ('zfs_handle_dup', 'zfs_handle_t *zfs_handle_dup(zfs_handle_t *);'),
    ('zfs_close', 'void zfs_close(zfs_handle_t *);'),
    ('zfs_get_type', 'zfs_type_t zfs_get_type(const zfs_handle_t *);'),
    ('zfs_get_name', 'const char *zfs_get_name(const zfs_handle_t *);'),
    ('zfs_get_pool_handle', 'zpool_handle_t *zfs_get_pool_handle(const zfs_handle_t *);'),
    ('zfs_prop_default_string', 'const char *zfs_prop_default_string(zfs_prop_t);'),
    ('zfs_prop_default_numeric', 'uint64_t zfs_prop_default_numeric(zfs_prop_t);'),
    ('zfs_prop_column_name', 'const char *zfs_prop_column_name(zfs_prop_t);'),
    ('zfs_prop_align_right', 'boolean_t zfs_prop_align_right(zfs_prop_t);'),
    ('zfs_valid_proplist', 'nvlist_t *zfs_valid_proplist(libzfs_handle_t *, zfs_type_t, nvlist_t *, uint64_t, zfs_handle_t *, const char *);'),
    ('zfs_prop_to_name', 'const char *zfs_prop_to_name(zfs_prop_t);'),
    ('zfs_prop_set', 'int zfs_prop_set(zfs_handle_t *, const char *, const char *);'),
    ('zfs_prop_get', 'int zfs_prop_get(zfs_handle_t *, zfs_prop_t, char *, size_t, zprop_source_t *, char *, size_t, boolean_t);'),
    ('zfs_prop_get_recvd', 'int zfs_prop_get_recvd(zfs_handle_t *, const char *, char *, size_t, boolean_t);'),
    ('zfs_prop_get_numeric', 'int zfs_prop_get_numeric(zfs_handle_t *, zfs_prop_t, uint64_t *, zprop_source_t *, char *, size_t);'),
    ('zfs_prop_get_userquota_int', 'int zfs_prop_get_userquota_int(zfs_handle_t *zhp, const char *propname, uint64_t *propvalue);'),
    ('zfs_prop_get_userquota', 'int zfs_prop_get_userquota(zfs_handle_t *zhp, const char *propname, char *propbuf, int proplen, boolean_t literal);'),
    ('zfs_prop_get_written_int', 'int zfs_prop_get_written_int(zfs_handle_t *zhp, const char *propname, uint64_t *propvalue);'),
    ('zfs_prop_get_written', 'int zfs_prop_get_written(zfs_handle_t *zhp, const char *propname, char *propbuf, int proplen, boolean_t literal);'),
    # ('zfs_prop_get_feature', 'int zfs_prop_get_feature(zfs_handle_t *zhp, const char *propname, char *buf, size_t len);'),  # TODO: Figure out why zfs_prop_get_feature causes an undefined symbol
    ('getprop_uint64', 'uint64_t getprop_uint64(zfs_handle_t *, zfs_prop_t, char **);'),
    ('zfs_prop_get_int', 'uint64_t zfs_prop_get_int(zfs_handle_t *, zfs_prop_t);'),
    ('zfs_prop_inherit', 'int zfs_prop_inherit(zfs_handle_t *, const char *, boolean_t);'),
    ('zfs_prop_values', 'const char *zfs_prop_values(zfs_prop_t);'),
    ('zfs_prop_is_string', 'int zfs_prop_is_string(zfs_prop_t prop);'),
    ('zfs_get_user_props', 'nvlist_t *zfs_get_user_props(zfs_handle_t *);'),
    # ('zfs_get_recvd_props', 'nvlist_t *zfs_get_recvd_props(zfs_handle_t *);'),  # TODO: Figure out why zfs_get_recvd_props causes an undefined symbol
    ('zfs_get_clones_nvl', 'nvlist_t *zfs_get_clones_nvl(zfs_handle_t *);'),
    ('zfs_expand_proplist', 'int zfs_expand_proplist(zfs_handle_t *, zprop_list_t **, boolean_t, boolean_t);'),
    ('zfs_prune_proplist', 'void zfs_prune_proplist(zfs_handle_t *, uint8_t *);'),
    ('zpool_expand_proplist', 'int zpool_expand_proplist(zpool_handle_t *, zprop_list_t **);'),
    ('zpool_prop_get_feature', 'int zpool_prop_get_feature(zpool_handle_t *, const char *, char *, size_t);'),
    ('zpool_prop_default_string', 'const char *zpool_prop_default_string(zpool_prop_t);'),
    ('zpool_prop_default_numeric', 'uint64_t zpool_prop_default_numeric(zpool_prop_t);'),
    ('zpool_prop_column_name', 'const char *zpool_prop_column_name(zpool_prop_t);'),
    ('zpool_prop_align_right', 'boolean_t zpool_prop_align_right(zpool_prop_t);'),
    ('zprop_iter', 'int zprop_iter(zprop_func func, void *cb, boolean_t show_all, boolean_t ordered, zfs_type_t type);'),
    ('zprop_get_list', 'int zprop_get_list(libzfs_handle_t *, char *, zprop_list_t **, zfs_type_t);'),
    ('zprop_free_list', 'void zprop_free_list(zprop_list_t *);'),
    ('zfs_iter_root', 'int zfs_iter_root(libzfs_handle_t *, zfs_iter_f, void *);'),
    ('zfs_iter_children', 'int zfs_iter_children(zfs_handle_t *, zfs_iter_f, void *);'),
    ('zfs_iter_dependents', 'int zfs_iter_dependents(zfs_handle_t *, boolean_t, zfs_iter_f, void *);'),
    ('zfs_iter_filesystems', 'int zfs_iter_filesystems(zfs_handle_t *, zfs_iter_f, void *);'),
    ('zfs_iter_snapshots', 'int zfs_iter_snapshots(zfs_handle_t *, boolean_t, zfs_iter_f, void *);'),
    ('zfs_iter_snapshots_sorted', 'int zfs_iter_snapshots_sorted(zfs_handle_t *, zfs_iter_f, void *);'),
    ('zfs_iter_snapspec', 'int zfs_iter_snapspec(zfs_handle_t *, const char *, zfs_iter_f, void *);'),
    ('zfs_create', 'int zfs_create(libzfs_handle_t *, const char *, zfs_type_t, nvlist_t *);'),
    ('zfs_create_ancestors', 'int zfs_create_ancestors(libzfs_handle_t *, const char *);'),
    ('zfs_destroy', 'int zfs_destroy(zfs_handle_t *, boolean_t);'),
    ('zfs_destroy_snaps', 'int zfs_destroy_snaps(zfs_handle_t *, char *, boolean_t);'),
    ('zfs_destroy_snaps_nvl', 'int zfs_destroy_snaps_nvl(libzfs_handle_t *, nvlist_t *, boolean_t);'),
    ('zfs_clone', 'int zfs_clone(zfs_handle_t *, const char *, nvlist_t *);'),
    ('zfs_snapshot', 'int zfs_snapshot(libzfs_handle_t *, const char *, boolean_t, nvlist_t *);'),
    ('zfs_snapshot_nvl', 'int zfs_snapshot_nvl(libzfs_handle_t *hdl, nvlist_t *snaps, nvlist_t *props);'),
    ('zfs_rollback', 'int zfs_rollback(zfs_handle_t *, zfs_handle_t *, boolean_t);'),
    ('zfs_rename', 'int zfs_rename(zfs_handle_t *, const char *, boolean_t, boolean_t);'),
    ('zfs_send', 'int zfs_send(zfs_handle_t *, const char *, const char *, sendflags_t *, int, snapfilter_cb_t, void *, nvlist_t **);'),
    ('zfs_promote', 'int zfs_promote(zfs_handle_t *);'),
    ('zfs_hold', 'int zfs_hold(zfs_handle_t *, const char *, const char *, boolean_t, int);'),
    ('zfs_hold_nvl', 'int zfs_hold_nvl(zfs_handle_t *, int, nvlist_t *);'),
    ('zfs_release', 'int zfs_release(zfs_handle_t *, const char *, const char *, boolean_t);'),
    ('zfs_get_holds', 'int zfs_get_holds(zfs_handle_t *, nvlist_t **);'),
    ('zvol_volsize_to_reservation', 'uint64_t zvol_volsize_to_reservation(uint64_t, nvlist_t *);'),
    # ('zfs_userspace', 'int zfs_userspace(zfs_handle_t *, zfs_userquota_prop_t, zfs_userspace_cb_t, void *);'),  # TODO: zfs_userspace_cb_t
    ('zfs_get_fsacl', 'int zfs_get_fsacl(zfs_handle_t *, nvlist_t **);'),
    ('zfs_set_fsacl', 'int zfs_set_fsacl(zfs_handle_t *, boolean_t, nvlist_t *);'),
    # ('zfs_receive', 'int zfs_receive(libzfs_handle_t *, const char *, recvflags_t *, int, avl_tree_t *);'),  # TODO: avl_tree_t
    ('zfs_show_diffs', 'int zfs_show_diffs(zfs_handle_t *, int, const char *, const char *, int);'),
    ('zfs_type_to_name', 'const char *zfs_type_to_name(zfs_type_t);'),
    ('zfs_refresh_properties', 'void zfs_refresh_properties(zfs_handle_t *);'),
    ('zfs_name_valid', 'int zfs_name_valid(const char *, zfs_type_t);'),
    ('zfs_path_to_zhandle', 'zfs_handle_t *zfs_path_to_zhandle(libzfs_handle_t *, char *, zfs_type_t);'),
    ('zfs_dataset_exists', 'boolean_t zfs_dataset_exists(libzfs_handle_t *, const char *, zfs_type_t);'),
    ('zfs_spa_version', 'int zfs_spa_version(zfs_handle_t *, int *);'),
    ('zfs_append_partition', 'int zfs_append_partition(char *path, size_t max_len);'),
    ('zfs_resolve_shortname', 'int zfs_resolve_shortname(const char *name, char *path, size_t pathlen);'),
    ('zfs_strcmp_pathname', 'int zfs_strcmp_pathname(char *name, char *cmp_name, int wholedisk);'),
    ('is_mounted', 'boolean_t is_mounted(libzfs_handle_t *, const char *special, char **);'),
    ('zfs_is_mounted', 'boolean_t zfs_is_mounted(zfs_handle_t *, char **);'),
    ('zfs_mount', 'int zfs_mount(zfs_handle_t *, const char *, int);'),
    ('zfs_unmount', 'int zfs_unmount(zfs_handle_t *, const char *, int);'),
    ('zfs_unmountall', 'int zfs_unmountall(zfs_handle_t *, int);'),
    ('zfs_is_shared', 'boolean_t zfs_is_shared(zfs_handle_t *);'),
    ('zfs_share', 'int zfs_share(zfs_handle_t *);'),
    ('zfs_unshare', 'int zfs_unshare(zfs_handle_t *);'),
    ('zfs_is_shared_nfs', 'boolean_t zfs_is_shared_nfs(zfs_handle_t *, char **);'),
    ('zfs_is_shared_smb', 'boolean_t zfs_is_shared_smb(zfs_handle_t *, char **);'),
    ('zfs_share_nfs', 'int zfs_share_nfs(zfs_handle_t *);'),
    ('zfs_share_smb', 'int zfs_share_smb(zfs_handle_t *);'),
    ('zfs_shareall', 'int zfs_shareall(zfs_handle_t *);'),
    ('zfs_unshare_nfs', 'int zfs_unshare_nfs(zfs_handle_t *, const char *);'),
    ('zfs_unshare_smb', 'int zfs_unshare_smb(zfs_handle_t *, const char *);'),
    ('zfs_unshareall_nfs', 'int zfs_unshareall_nfs(zfs_handle_t *);'),
    ('zfs_unshareall_smb', 'int zfs_unshareall_smb(zfs_handle_t *);'),
    ('zfs_unshareall_bypath', 'int zfs_unshareall_bypath(zfs_handle_t *, const char *);'),
    ('zfs_unshareall', 'int zfs_unshareall(zfs_handle_t *);'),
    # ('zfs_deleg_share_nfs', 'int zfs_deleg_share_nfs(libzfs_handle_t *, char *, char *, char *, void *, void *, int, zfs_share_op_t);'),  # TODO: Figure out why zfs_deleg_share_nfs causes an undefined symbol
    ('zfs_nicenum', 'void zfs_nicenum(uint64_t, char *, size_t);'),
    ('zfs_nicestrtonum', 'int zfs_nicestrtonum(libzfs_handle_t *, const char *, uint64_t *);'),
    ('zpool_in_use', 'int zpool_in_use(libzfs_handle_t *, int, pool_state_t *, char **, boolean_t *);'),
    ('zpool_read_label', 'int zpool_read_label(int, nvlist_t **);'),
    ('zpool_clear_label', 'int zpool_clear_label(int);'),
    ('zpool_enable_datasets', 'int zpool_enable_datasets(zpool_handle_t *, const char *, int);'),
    ('zpool_disable_datasets', 'int zpool_disable_datasets(zpool_handle_t *, boolean_t);'),
])

VERSION_SPECIFIC = {
    "0.6.2": [

    ]
}
