# Copyright (C) 2013-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=invalid-name,line-too-long

# Author: Wlodzimierz Wencel

# This file contains a number of common steps that are general and may be used
# By a lot of feature files.
#

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

    # clear all config files
    world.ddns_cfg = {}
    world.dhcp_cfg = {"option-data": [],
                      "hooks-libraries": [],
                      "shared-networks": []}
    world.ca_cfg = {}
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
                    world.prl = "" # don't request anything by default

            if world.proto == "v6":
                # Start with fresh, empty ORO (v6)
                if hasattr(world, 'oro'):
                    world.oro = DHCP6OptOptReq()
                    # Scapy creates ORO with 23, 24 options request. Let's get rid of them
                    world.oro.reqopts = [] # don't request anything by default

            # some tests skip "test setup" procedure and goes to "test procedure"
            # e.g. tests for server configuration. Then we need to setup
            # world.kea["option_cnt"] here.
            # TODO this will probably mess up access to configuration dict from within the test
            set_world()
        else:
            pass
