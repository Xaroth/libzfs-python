#include <libzfs.h>
#include <libnvpair.h>
#include <sys/fs/zfs.h>
#include <sys/types.h>

/*
 * A small workaround.
 *  python-cffi does not allow ffi.addressof(<pointer>).. so using libzfs'
 *  method of newconfig = zpool_get_config(zhp, &oldconfig) won't work nicely
 *  instead, we create our own zpool_get_old_config function that pretty
 *  much does the same.
 */
nvlist_t *zpool_get_old_config(zpool_handle_t *zhp) {
    nvlist_t *oldconfig, *newconfig;
    newconfig = zpool_get_config(zhp, &oldconfig);
    return (oldconfig);
}
