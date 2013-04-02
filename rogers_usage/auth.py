""" Common module for loading authorization info """

import json
import os.path

from collections import namedtuple

from xdg.BaseDirectory import load_first_config

AuthInfo = namedtuple('AuthInfo', ['username', 'password'])

def get_auth_info():
    config_dir = load_first_config('rogers-usage')
    with open(os.path.join(config_dir, 'auth.json'), 'rb') as fh:
        info = json.loads(fh.read())
        if info:
            return AuthInfo(info['username'], info['password'])
        else:
            # Maybe throw an exception?
            return AuthInfo(None, None)
