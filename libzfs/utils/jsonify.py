from . import six

from enum import Enum
from json import JSONEncoder

PARSE_KEEP = 0
PARSE_NAME = 1
PARSE_NAME_LONG = 2
PARSE_VALUE = 3
PARSE_BOTH = 4


def _parse_enum(o, parse_enums=PARSE_KEEP):
    if parse_enums == PARSE_NAME:
        return o.name
    elif parse_enums == PARSE_NAME_LONG:
        return str(o)
    elif parse_enums == PARSE_VALUE:
        return o.value
    elif parse_enums == PARSE_BOTH:
        return {'name': o.name, 'value': o.value}
    return o


def jsonify(o, max_depth=-1, parse_enums=PARSE_KEEP):
    """
    Walks through object o, and attempts to get the property instead of the key, if available.
    This means that for our VDev objects we can easily get a dict of all the 'parsed' values.
    """
    if max_depth == 0:
        return o
    max_depth -= 1
    if isinstance(o, dict):
        def _getter(key, value):
            other = getattr(o, key, value)
            if callable(other):
                other = value
            return value
        return {key: jsonify(_getter(key, value), max_depth=max_depth, parse_enums=parse_enums)
                for key, value in six.iteritems(o)}
    elif isinstance(o, list):
        return [jsonify(x, max_depth=max_depth, parse_enums=parse_enums) for x in o]
    elif isinstance(o, tuple):
        return (jsonify(x, max_depth=max_depth, parse_enums=parse_enums) for x in o)
    elif isinstance(o, Enum):
        o = _parse_enum(o)
    return o


class LibZFSJSONEncoder(JSONEncoder):
    def __init__(self, parse_enums=PARSE_BOTH, *args, **kwargs):
        self.parse_enums = parse_enums
        super(LibZFSJSONEncoder, self).__init__(*args, **kwargs)

    def iterencode(self, o, _one_shot=False):
        o = jsonify(o, parse_enums=self.parse_enums)
        return super(LibZFSJSONEncoder, self).iterencode(o)


__all__ = [
    'LibZFSJSONEncoder',
    'jsonify',
    'PARSE_KEEP',
    'PARSE_NAME',
    'PARSE_NAME_LONG',
    'PARSE_VALUE',
    'PARSE_BOTH',
]
