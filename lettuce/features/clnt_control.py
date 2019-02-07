# Copyright (C) 2014 Internet Systems Consortium.
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

# Author: Maciek Fijalkowski

import sys
import importlib

from forge import world, step
from terrain import declare_all


############################################################################
#from init_all import SOFTWARE_UNDER_TEST, DHCP
#TODO That import have to be switched to ForgeConfiguration class, world.f_cfg
SOFTWARE_UNDER_TEST = ""
DHCP = ""
############################################################################

declare_all()
DNS = ""
for each_client_name in SOFTWARE_UNDER_TEST:
    if each_client_name in DHCP and "client" in each_client_name:
        dhcp = importlib.import_module("softwaresupport.%s.functions" % each_client_name)
        world.cfg["dhcp_under_test"] = each_client_name
    elif each_client_name in DNS:
        # for future use, import DNS not declare it.
        pass


"""
Step provides client initialization. Needs to be included before
step "Client is started."
"""
@step("Setting up test.")
def client_setup():
    dhcp.client_setup()


"""
Step executes a command specific to currently tested software, which
results in running a client on DUT.
"""
@step("Client is started.")
def client_start():
    dhcp.start_clnt()


"""
This step adds another client option to a config that is being generated.
Supported options may differ for particular implementation. Please see
in softwaresupport/SOFTWARE_UNDER_TEST/functions.py file what options
you can include with this step.
"""
@step("Client is configured to include (another )?(\S+) option.")
def client_option_req(another, opt):
    another1 = (another == "another ")
    dhcp.client_option_req(another1, opt)


"""
Step executes a commands that result in restarting client on DUT.
"""
@step("Restart client.")
def client_restart():
    dhcp.restart_clnt()


"""
Step provides following functionality:
- download a lease (or config) file that was created by specific software
  on DUT,
- create a proper structure (dictionary) from downloaded file,
- compare created structure with structure from REPLY message.

Step checks whether client uses a configuration parameters given by server.
Currently, this step supports only IA_PDs. Support for IA_NAs should be
provided also.
"""
@step("Client MUST (NOT )?use prefix with values given by server.")
def client_parse_config(yes_no):
    contain = not (yes_no == "NOT ")
    dhcp.client_parse_config(contain)
