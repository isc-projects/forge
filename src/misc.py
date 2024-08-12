# Copyright (C) 2013-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Wlodzimierz Wencel

# This file contains a number of common steps that are general and may be used
# By a lot of feature files.

# pylint: disable=consider-using-enumerate
# pylint: disable=invalid-name
# pylint: disable=superfluous-parens

from scapy.layers.dhcp6 import DHCP6OptOptReq

from .forge_cfg import world, step
from .softwaresupport.configuration import KeaConfiguration


def set_world():
    """
    Set counters which are being used to server configuration in Kea
    """
    if not hasattr(world, 'dhcp'):
        world.dhcp = {}
    else:
        world.dhcp.clear()

    world.dhcp["option_cnt"] = 0
    world.dhcp["subnet_cnt"] = 0
    world.dhcp["option_usr_cnt"] = 0
    world.f_cfg.auto_multi_threading_configuration = True

    # clear all config files
    world.ddns_cfg = {}
    world.dhcp_cfg = {"option-data": [],
                      "hooks-libraries": [],
                      "shared-networks": []}
    world.ca_cfg = {"Control-agent": {}}
    if "isc_dhcp" in world.cfg["dhcp_under_test"]:
        world.subcfg = [["", "", "", "", "", "", ""]]
        world.cfg["conf_time"] = ""
    # new configuration process:
    world.configClass = KeaConfiguration()


@step(r'Pass Criteria:')
def pass_criteria():
    # Do nothing, "Pass criteria:" appears in the text as beautification only
    pass


@step(r'Test Setup:')
def test_setup():
    set_world()


@step(r'Server reconfigure:')
def reconfigure():
    set_world()


@step(r'Test Procedure:')
def test_procedure():
    for each in world.f_cfg.software_under_test:
        if "server" in each:
            if world.proto == "v4":
                # Start with fresh, empty PRL (v4)
                if hasattr(world, 'prl'):
                    world.prl = ""  # don't request anything by default

            if world.proto == "v6":
                # Start with fresh, empty ORO (v6)
                if hasattr(world, 'oro'):
                    world.oro = DHCP6OptOptReq()
                    # Scapy creates ORO with 23, 24 options request. Let's get rid of them
                    world.oro.reqopts = []  # don't request anything by default

            # some tests skip "test setup" procedure and goes to "test procedure"
            # e.g. tests for server configuration. Then we need to setup
            # world.kea["option_cnt"] here.
            # TODO this will probably mess up access to configuration dict from within the test
            set_world()
        else:
            pass


def merge_containers(target, source, identify=None, last_list_parent_key=None):
    """
    Recursively merges dicts and lists from {source} into {target}.
    :param target: container being merged into
    :param source: container being merged
    :param identify: dict used to uniquely identify elements within the source and target lists that
                     are being merged. Keys in this dict are so-called last-list-parent-keys - a way
                     to limit the places where these unique keys are considered. Values in this dict
                     are the unique IDs for the elements in the source and target lists being
                     merged. By default None which means no smart merging is attempted.
                     E.g. {'output-options': 'output'} for:
                     {
                         "name": "kea-dhcp6",
                         "output-options": [
                             {
                                 "output": "/opt/kea/var/log/kea.log",
                                 "flush": true,
                                 "maxsize": 10240000,
                                 "maxver": 1,
                                 "pattern": ""
                             }
                         ],
                         "debuglevel": 99,
                         "severity": "DEBUG"
                     }
    :param last_list_parent_key: The last dict key that hosted a list in the recursive path. This
                                 will be matched against keys in {identify}. Only for internal
                                 recursive calls. Don't set this explicitly from external calls.

    """
    if (isinstance(target, dict)):
        for k, v in source.items():
            if (k in target and isinstance(target[k], dict) and isinstance(v, dict)):
                merge_containers(target[k], v, identify, k)
            elif (k in target and isinstance(target[k], list) and isinstance(v, list)):
                merge_containers(target[k], v, identify, k)
            else:
                target[k] = v
    elif (isinstance(target, list)):
        if identify is not None and last_list_parent_key is not None and last_list_parent_key in identify:
            # We have information about what to merge.
            list_id = identify[last_list_parent_key]
            for (s, t) in [(s, t) for s in source for t in target if s[list_id] == t[list_id]]:
                merge_containers(t, s, identify, None)
                break
        else:
            # No information about what to merge. Just do a best-effort approach
            # and add source elements to target if they are not already there.
            for s in source:
                if (s not in target):
                    target.append(s)
