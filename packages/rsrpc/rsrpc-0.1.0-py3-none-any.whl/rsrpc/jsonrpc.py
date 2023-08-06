# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import requests

from .json import dumps, load_objhook

# -------------------------------------------------------------------------------------------------------------------- #

class Client:

    def __init__(self, url: str, *, timeout: int|float=30):
        ''' init client '''
        self.url = url
        self.timeout = timeout


    def call(self, method: str, *args, **kw):
        ''' call jsonrpc method '''

        if args and kw:
            raise ValueError('can not pass both args and kw')
        elif args:
            params = args
        else:
            params = kw

        r = requests.post(self.url, data=dumps({
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
        }), timeout=self.timeout)
        r.raise_for_status()

        r = r.json(object_hook=load_objhook)
        if 'error' in r:
            raise RPCError(r['error'])
        return r['result']

# -------------------------------------------------------------------------------------------------------------------- #

class RPCError(Exception):

    def __init__(self, error: dict):
        super().__init__()
        self.code = error['code']
        self.msg = error['message']

    def __str__(self):
        return f'RPCError {self.code:d}: {self.msg}'

# -------------------------------------------------------------------------------------------------------------------- #
