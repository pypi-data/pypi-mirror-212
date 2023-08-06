# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from base64 import a85decode, a85encode
from datetime import date, datetime, time
from decimal import Decimal
import json

# -------------------------------------------------------------------------------------------------------------------- #

DECODERS = {
    'bin':  a85decode,
    'date': date.fromisoformat,
    'dec':  Decimal,
    'dt':   datetime.fromisoformat,
    'time': time.fromisoformat,
}

# -------------------------------------------------------------------------------------------------------------------- #

ENCODERS = {
    bytes:      ('bin', lambda obj: a85encode(obj).decode('ascii')),
    date:       ('date', str),
    datetime:   ('dt', lambda obj: obj.isoformat()),
    Decimal:    ('dec', str),
    memoryview: ('bin', lambda obj: a85encode(obj).decode('ascii')),
    time:       ('time', str),
}

# -------------------------------------------------------------------------------------------------------------------- #

def load(*args, **kw):
    return json.load(*args, object_hook=load_objhook, **kw)

def loads(*args, **kw):
    return json.loads(*args, object_hook=load_objhook, **kw)


def load_objhook(obj):
    d = DECODERS.get(obj.get('$t'))
    if d is not None and '$v' in obj:
        return d(obj['$v'])
    return obj

# -------------------------------------------------------------------------------------------------------------------- #

def dump(*args, **kw):
    return json.dump(*args, default=dump_default, **kw)

def dumps(*args, **kw):
    return json.dumps(*args, default=dump_default, **kw)


def dump_default(obj):
    e = ENCODERS.get(type(obj))
    if e is not None:
        return {'$t': e[0], '$v': e[1](obj)}
    return obj

# -------------------------------------------------------------------------------------------------------------------- #
