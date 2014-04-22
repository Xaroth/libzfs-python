from .enums import data_type
from .cdefs import TYPEDEFS, FUNCTIONS, VERSION_SPECIFIC

INCLUDES = ['general']
GENERATE = True

__all__ = [
    'data_type',

    'TYPEDEFS',
    'FUNCTIONS',
    'INCLUDES',
    'VERSION_SPECIFIC',
]
