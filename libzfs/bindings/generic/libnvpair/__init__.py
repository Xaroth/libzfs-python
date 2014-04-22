from .enums import DataType
from .cdefs import TYPEDEFS, FUNCTIONS, VERSION_SPECIFIC

INCLUDES = ['general']
GENERATE = True

__all__ = [
    'DataType',

    'TYPEDEFS',
    'FUNCTIONS',
    'INCLUDES',
    'VERSION_SPECIFIC',
]
