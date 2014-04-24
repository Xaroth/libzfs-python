libzfs handle
=============

As with most libraries, libzfs stores it's information in in its own structure, allowing external libraries (like libzfs-python) access through exposed functions and handles.

For developers using this library, it's needed to obtain a handle, and ensure that it is disposed of when done with it, so libzfs-python offers a quick and easy method of doing just that.

.. autoclass:: libzfs.LibZFSHandle
   :members:
   :undoc-members:
