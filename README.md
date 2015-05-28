libzfs-python
=============

The goal of libzfs-python is to provide both low-level access to libzfs' inner workings from within python, as well as providing a set of useful (pythonic) interfaces to obtaining data from libzfs.

CFFI allows us to provide a raw interface into libzfs, so that we do not have to rely on external applications to provide us information about the status and configuration of ZFS on the running system, making it suitable for both monitoring, and interfacing with ZFS.


Requirements
============

Currently, libzfs-python requires the CFFI module to be installed (which can easily be installed through ``pip`` or ``easy_install``). Furthermore, libzfs' header files have to be available on your system (which can usually be obtained by installing the libzfs-dev package on your system, if not already available).

The main python version being developed for is 2.7, however, the long-term goal is to also support 3.4+ and PyPy.

Installation
============

libzfs-python requires CFFI version 1.0 or higher to be installed (due to the changes in CFFI's compile mechanisms released with that version). During the installation of the package the cffi bindings will automatically be built.

If/when you update zfs on your system, it is wise to re-install libzfs-python to ensure it is correctly compiled against the currently installed libzfs version.
