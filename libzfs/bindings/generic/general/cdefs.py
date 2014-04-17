from collections import OrderedDict

TYPEDEFS = OrderedDict([
    ('boolean_t',    'typedef enum { B_FALSE, B_TRUE } boolean_t;',),
    ('uchar_t',      'typedef unsigned char uchar_t;',),
    ('ushort_t',     'typedef unsigned short ushort_t;',),
    ('uint_t',       'typedef unsigned int uint_t;',),
    ('ulong_t',      'typedef unsigned long ulong_t;',),
    ('longlong_t',   'typedef long long longlong_t;',),
    ('hrtime_t',     'typedef longlong_t hrtime_t;',),
])

FUNCTIONS = OrderedDict()
