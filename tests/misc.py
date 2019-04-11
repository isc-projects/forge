# Copyright (C) 2013-2017 Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: Wlodzimierz Wencel

# This file contains a number of common steps that are general and may be used
# By a lot of feature files.
#

import sys

from scapy.layers.dhcp6 import DHCP6OptOptReq

from forge_cfg import world, step
from softwaresupport.configuration import KeaConfiguration


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
    world.cfg["conf"] = ""
    world.subcfg = [["", "", "", "", "", "", ""]]  # additional config structure
    world.shared_subcfg = []
    world.shared_subnets = []
    world.shared_subnets_tmp = []
    world.kea_ha = [[], [], [], []]
    world.hooks = []
    world.classification = []

    # new configuration process:
    world.configClass = KeaConfiguration()


@step('Pass Criteria:')
def pass_criteria():
    # Do nothing, "Pass criteria:" appears in the text as beautification only
    pass


@step('Test Setup:')
def test_setup():
    set_world()


@step('Server reconfigure:')
def reconfigure():
    set_world()


@step('Test Procedure:')
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
            set_world()
        else:
            pass
