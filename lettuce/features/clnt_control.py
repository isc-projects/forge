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


from lettuce import world, step
from init_all import SOFTWARE_UNDER_TEST
import importlib

clntFunc = importlib.import_module("softwaresupport.%s.functions"  % SOFTWARE_UNDER_TEST)


@step("Setting up test.")
def client_setup(step):
    clntFunc.client_setup(step)

@step('Client is started.')
def config_srv_subnet(step):
   clntFunc.start_clnt(step)

@step("Client is configured to include (another )?(\S+) option.")
def client_option_req(step, another, opt):
    another1 = (another == "another ")
    clntFunc.client_option_req(step, another1, opt)

@step("Restart client.")
def client_restart(step):
    clntFunc.restart_clnt(step)

@step("Client MUST (NOT )?use prefix with values given by server.")
def client_parse_config(step, yes_no):
    contain = not (yes_no == "NOT ")
    clntFunc.client_parse_config(step, contain)
