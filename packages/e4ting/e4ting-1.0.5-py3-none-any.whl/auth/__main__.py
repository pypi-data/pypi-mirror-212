#!/usr/bin/python
# -*- coding: utf-8 -*-
#!/bin/env python3
# -*- coding:utf-8 -*-

from pdb import set_trace as strace
import time
import json
import sys,os

from pdb import set_trace as strace
from traceback  import format_exc as dumpstack

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

import util
from webcontainer import init,run

import webauth

def main(option):

    version = option.version
    api,app = init("auth", option)
    # strace()
    api.add_resource(webauth.LOGIN,
        "/{version}/api/auth".format(version=version),
        "/{version}/api/auth/".format(version=version)
        )
    util.log(webauth.LOGIN,
        "/{version}/api/auth".format(version=version),
            "/{version}/api/auth/".format(version=version))
    api.add_resource(webauth.REGISTER,
        "/{version}/api/register".format(version=version),
        "/{version}/api/register/".format(version=version)
        )
    api.add_resource(webauth.LOGOUT,
        "/{version}/api/logout".format(version=version)
        )

    run(app)

if __name__ == '__main__':
    main( util.argv_parse() )