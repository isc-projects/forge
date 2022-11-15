# Copyright (C) 2021-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=unused-import

import sys

import Crypto
import fabric
import netifaces
import pytest
import requests
import scapy


def _get_version(module):
    if hasattr(module, '__version__'):
        return module.__version__
    if hasattr(module, 'version'):
        if hasattr(module.version, '__version__'):
            return module.version.__version__
        return module.version
    return 'unknown'


def print_versions():
    print('Dependency versions:')
    for i in [sys.modules[name] for name in sorted(set(sys.modules) & set(globals()) - {'sys'})]:
        print(f"  * {i.__name__ if hasattr(i, '__name__') else 'unknown'}: {_get_version(i)}")
