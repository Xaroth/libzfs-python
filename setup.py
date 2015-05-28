from setuptools import setup, find_packages, findall
from setuptools.command.install import install
import sys
import os
from os.path import join, abspath, dirname

NAME = "libzfs"
VERBOSE_NAME = "libzfs"

DESC = """
Python CFFI bindings for libzfs
"""

AUTHOR_NAME = "Steven 'Xaroth' Noorbergen"
AUTHOR_EMAIL = "devnull@xaroth.nl"
AUTHOR_URL = "www.xaroth.nl"


classes = """
    Development Status :: 2 - Pre-Alpha
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent
    Operating System :: POSIX
    Operating System :: Unix
    Programming Language :: Python
    Programming Language :: Python :: 2
    Programming Language :: Python :: 2.6
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.3
    Programming Language :: Python :: Implementation :: CPython
    Programming Language :: Python :: Implementation :: PyPy
    Programming Language :: Python :: Implementation :: Jython
    Topic :: Software Development :: Libraries :: Python Modules
    Topic :: System :: Systems Administration
    Topic :: Utilities
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

PY3 = sys.version_info[0] == 3
JYTHON = sys.platform.startswith('java')
PYPY = hasattr(sys, 'pypy_version_info')


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def reqs():
    try:
        return [
            r for r in (
                strip_comments(l) for l in open(
                    os.path.join(os.getcwd(), 'requirements.txt')).readlines()
            ) if r]
    except:
        return []

install_requires = reqs()

entrypoints = {}
extra = {}

console_scripts = entrypoints['console_scripts'] = [
]

import libzfs
VERSION = libzfs.__version__

if os.environ.get('SETUP_NORUN'):
    setup = lambda *args, **kwargs: None  # noqa


setup(
    name=NAME,
    version=VERSION,
    description=DESC,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    url=AUTHOR_URL,
    platforms=['any'],
    license='MIT License',
    packages=find_packages(exclude=['tests', 'tests.*', 'docs', 'docs.*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    classifiers=classifiers,
    entry_points=entrypoints,
    long_description=DESC,
    extras_require={},
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=['build_bindings.py:ffi'],
    **extra)
