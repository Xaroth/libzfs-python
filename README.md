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

libzfs-python uses ``setuptools`` to install, however, there is one small twist.

Since libzfs' interface can change between versions, it is possible to specify the ``LIBZFS_VERSION`` environment variable while running ``python setup.py install``, to force the library to keep that version in mind.

This, however, does also mean that, when you update libzfs, you will need to reinstall libzfs-python (as the new binding module will have to be compiled).

The version specified during install (or the configured latest version in the code) can be retrieved by the following code:

````
>>> import libzfs
>>> print(libzfs.libzfs_version)
0.6.2
````
