# Copyright (C) 2013-2022 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""DHCPv4 leasequery tests"""

import pytest

from src import srv_control
from src import misc
from src import srv_msg
from src.forge_cfg import world


@pytest.mark.v4
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('rai_version', ['old-RAI', 'new-RAI'])
def test_v4_leasequery_ip(backend, rai_version):
    """
    Test of v4 lease query messages asking for ip address.
    Test sends queries to trigger "leaseunknown", "leaseunassigned", and "leaseactive" responses.
    :param backend:
    """

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # adding hook and required parameters
    srv_control.add_hooks('libdhcp_lease_query.so')
    # Set permitted requester to forge machine ip
    world.dhcp_cfg["hooks-libraries"][0].update({"parameters": {"requesters": ["$(CIADDR)"]}})
    world.cfg["source_port"] = 67

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # Building lease query message to ask for ip-address outside of subnet
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(CIADDR)')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.51.1')
    srv_msg.client_sets_value('Client', 'htype', 0)
    srv_msg.client_sets_value('Client', 'chaddr', "00")
    srv_msg.client_sets_value('Client', 'hlen', 0)
    srv_msg.client_send_msg('LEASEQUERY')

    # sending and testing the response
    srv_msg.send_wait_for_message('MUST', 'LEASEUNKNOWN')
    srv_msg.response_check_content('ciaddr', '192.168.51.1')
    srv_msg.response_check_include_option(53)
    srv_msg.response_check_option_content(53, 'value', 12)

    # Building lease query message to ask by ip-address about free lease
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(CIADDR)')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'htype', 0)
    srv_msg.client_sets_value('Client', 'chaddr', "00")
    srv_msg.client_sets_value('Client', 'hlen', 0)
    srv_msg.client_send_msg('LEASEQUERY')

    # sending and testing the response
    srv_msg.send_wait_for_message('MUST', 'LEASEUNASSIGNED')
    srv_msg.response_check_content('ciaddr', '192.168.50.1')
    srv_msg.response_check_include_option(53)
    srv_msg.response_check_option_content(53, 'value', 11)

    if rai_version == 'old-RAI':
        rai = "0x0106060106020603"
    else:
        rai = {"sub-options": "0x0106060106020603"}

    # add a lease
    cmd = {"command": "lease4-add",
           "arguments": {"ip-address": "192.168.50.1",
                         "hw-address": "1a:1b:1c:1d:1e:1f",
                         "client-id": '0x00010203040506',
                         "user-context": {
                           "ISC": {
                             "relay-agent-info": rai
                           }
                         }}}
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Building lease query message to ask by ip-address about taken lease
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(CIADDR)')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'htype', 0)
    srv_msg.client_sets_value('Client', 'chaddr', "00")
    srv_msg.client_sets_value('Client', 'hlen', 0)
    srv_msg.client_requests_option(82)
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEACTIVE')
    srv_msg.response_check_content('chaddr', "1a:1b:1c:1d:1e:1f")
    srv_msg.response_check_content('ciaddr', "192.168.50.1")
    srv_msg.response_check_include_option(61)  # dhcp-client-identifier
    srv_msg.response_check_option_content(61, 'value', '00010203040506')
    srv_msg.response_check_include_option(53)  # DHCP Message Type
    srv_msg.response_check_option_content(53, 'value', 13)  # Lease Active
    srv_msg.response_check_include_option(82)  # dhcp-agent-options
    srv_msg.response_check_option_content(82, 'value', b'\x01\x06\x06\x01\x06\x02\x06\x03')
    srv_msg.response_check_include_option(51)  # dhcp-lease-time
    srv_msg.response_check_include_option(58)  # dhcp-renewal-time
    srv_msg.response_check_include_option(59)  # dhcp-rebind-time
    srv_msg.response_check_include_option(91)  # client-last-transaction-time


@pytest.mark.v4
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('rai_version', ['old-RAI', 'new-RAI'])
def test_v4_leasequery_mac(backend, rai_version):
    """
    Test of v4 lease query messages asking for mac address.
    Test sends queries to trigger "leaseunknown" and "leaseactive" responses.
    :param backend:
    """

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_another_subnet_no_interface('192.168.60.0/24',
                                                       '192.168.60.0-192.168.60.1')
    srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # adding hook and required parameters
    srv_control.add_hooks('libdhcp_lease_query.so')
    # Set permitted requester to forge machine ip
    world.dhcp_cfg["hooks-libraries"][0].update({"parameters": {"requesters": ["$(CIADDR)"]}})
    world.cfg["source_port"] = 67

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # Building lease query message to ask for unknown mac address
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(CIADDR)')
    srv_msg.client_sets_value('Client', 'ciaddr', 0)
    srv_msg.client_sets_value('Client', 'chaddr', "1a:1b:1c:1d:1e:1f")
    srv_msg.client_send_msg('LEASEQUERY')

    # sending and testing the response
    srv_msg.send_wait_for_message('MUST', 'LEASEUNKNOWN')
    srv_msg.response_check_content('chaddr', "1a:1b:1c:1d:1e:1f")
    srv_msg.response_check_include_option(53)
    srv_msg.response_check_option_content(53, 'value', 12)

    if rai_version == 'old-RAI':
        rai = "0x0106060106020603"
    else:
        rai = {"sub-options": "0x0106060106020603"}

    # add a lease
    cmd = {"command": "lease4-add",
           "arguments": {"ip-address": "192.168.50.1",
                         "hw-address": "1a:1b:1c:1d:1e:1f",
                         "client-id": '0x00010203040506',
                         "user-context": {
                           "ISC": {
                             "relay-agent-info": rai
                           }
                         }}}
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    if rai_version == 'old-RAI':
        rai = "0x0106060106020603"
    else:
        rai = {"sub-options": "0x0106060106020603"}

    # add second lease for same client
    cmd = {"command": "lease4-add",
           "arguments": {"ip-address": "192.168.60.1",
                         "hw-address": "1a:1b:1c:1d:1e:1f",
                         "client-id": '0x00010203040506',
                         "user-context": {
                           "ISC": {
                             "relay-agent-info": rai
                           }
                         }}}
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Building lease query message to ask for added lease
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(CIADDR)')
    srv_msg.client_sets_value('Client', 'ciaddr', 0)
    srv_msg.client_sets_value('Client', 'chaddr', "1a:1b:1c:1d:1e:1f")
    srv_msg.client_requests_option(82)  # Recommended by RFC, not required by Kea
    srv_msg.client_send_msg('LEASEQUERY')

    # sending and testing the response
    srv_msg.send_wait_for_message('MUST', 'LEASEACTIVE')
    srv_msg.response_check_content('chaddr', "1a:1b:1c:1d:1e:1f")
    srv_msg.response_check_content('ciaddr', "192.168.50.1")
    srv_msg.response_check_include_option(61)  # dhcp-client-identifier
    srv_msg.response_check_option_content(61, 'value', '00010203040506')
    srv_msg.response_check_include_option(53)  # DHCP Message Type
    srv_msg.response_check_option_content(53, 'value', 13)  # Lease Active
    srv_msg.response_check_include_option(82)  # dhcp-agent-options
    srv_msg.response_check_option_content(82, 'value', b'\x01\x06\x06\x01\x06\x02\x06\x03')
    srv_msg.response_check_include_option(51)  # dhcp-lease-time
    srv_msg.response_check_include_option(58)  # dhcp-renewal-time
    srv_msg.response_check_include_option(59)  # dhcp-rebind-time
    srv_msg.response_check_include_option(91)  # client-last-transaction-time
    srv_msg.response_check_include_option(92)  # associated-ip
    srv_msg.response_check_option_content(92, 'value', '192.168.60.1')  # second lease


@pytest.mark.v4
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('rai_version', ['old-RAI', 'new-RAI'])
def test_v4_leasequery_client(backend, rai_version):
    """
    Test of v4 lease query messages asking for client id
    Test sends queries to trigger "leaseunknown" and "leaseactive" responses.
    :param backend:
    """

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_another_subnet_no_interface('192.168.60.0/24',
                                                       '192.168.60.0-192.168.60.1')
    srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # adding hook and required parameters
    srv_control.add_hooks('libdhcp_lease_query.so')
    # Set permitted requester to forge machine ip
    world.dhcp_cfg["hooks-libraries"][0].update({"parameters": {"requesters": ["$(CIADDR)"]}})
    world.cfg["source_port"] = 67

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # Building lease query message to ask for unknown client-id
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(CIADDR)')
    srv_msg.client_sets_value('Client', 'ciaddr', 0)
    srv_msg.client_sets_value('Client', 'htype', 0)
    srv_msg.client_sets_value('Client', 'chaddr', "00")
    srv_msg.client_sets_value('Client', 'hlen', 0)
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_send_msg('LEASEQUERY')

    # sending and testing the response
    srv_msg.send_wait_for_message('MUST', 'LEASEUNKNOWN')
    srv_msg.response_check_option_content(61, 'value', '00010203040506')
    srv_msg.response_check_include_option(53)
    srv_msg.response_check_option_content(53, 'value', 12)

    if rai_version == 'old-RAI':
        rai = "0x0106060106020603"
    else:
        rai = {"sub-options": "0x0106060106020603"}

    # add a lease
    cmd = {"command": "lease4-add",
           "arguments": {"ip-address": "192.168.50.1",
                         "hw-address": "1a:1b:1c:1d:1e:1f",
                         "client-id": '0x00010203040506',
                         "user-context": {
                           "ISC": {
                             "relay-agent-info": rai
                           }
                         }}}
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    if rai_version == 'old-RAI':
        rai = "0x0106060106020603"
    else:
        rai = {"sub-options": "0x0106060106020603"}

    # add second lease for same client
    cmd = {"command": "lease4-add",
           "arguments": {"ip-address": "192.168.60.1",
                         "hw-address": "1a:1b:1c:1d:1e:1f",
                         "client-id": '0x00010203040506',
                         "user-context": {
                           "ISC": {
                             "relay-agent-info": rai
                           }
                         }}}
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    # Building lease query message to ask for added client-id
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(CIADDR)')
    srv_msg.client_sets_value('Client', 'ciaddr', 0)
    srv_msg.client_sets_value('Client', 'htype', 0)
    srv_msg.client_sets_value('Client', 'chaddr', "00")
    srv_msg.client_sets_value('Client', 'hlen', 0)
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_requests_option(82)  # Recommended by RFC, not required by Kea
    srv_msg.client_send_msg('LEASEQUERY')

    # sending and testing the response
    srv_msg.send_wait_for_message('MUST', 'LEASEACTIVE')
    srv_msg.response_check_content('chaddr', "1a:1b:1c:1d:1e:1f")
    srv_msg.response_check_content('ciaddr', "192.168.50.1")
    srv_msg.response_check_include_option(61)  # dhcp-client-identifier
    srv_msg.response_check_option_content(61, 'value', '00010203040506')
    srv_msg.response_check_include_option(53)  # DHCP Message Type
    srv_msg.response_check_option_content(53, 'value', 13)  # Lease Active
    srv_msg.response_check_include_option(82)  # dhcp-agent-options
    srv_msg.response_check_option_content(82, 'value', b'\x01\x06\x06\x01\x06\x02\x06\x03')
    srv_msg.response_check_include_option(51)  # dhcp-lease-time
    srv_msg.response_check_include_option(58)  # dhcp-renewal-time
    srv_msg.response_check_include_option(59)  # dhcp-rebind-time
    srv_msg.response_check_include_option(91)  # client-last-transaction-time
    srv_msg.response_check_include_option(92)  # associated-ip
    srv_msg.response_check_option_content(92, 'value', '192.168.60.1')  # second lease


@pytest.mark.v4
@pytest.mark.hook
def test_v4_leasequery_denied():
    """
    Test to confirm Kea will not answer to lease query from denied requester.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # adding hook and required parameters
    srv_control.add_hooks('libdhcp_lease_query.so')
    # Adding different ip than forge machine
    world.dhcp_cfg["hooks-libraries"][0].update({"parameters": {"requesters": ["$(MGMT_ADDRESS)"]}})
    world.cfg["source_port"] = 67

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # Building lease query message to ask for ip-address
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(CIADDR)')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'htype', 0)
    srv_msg.client_sets_value('Client', 'chaddr', "00")
    srv_msg.client_sets_value('Client', 'hlen', 0)
    srv_msg.client_send_msg('LEASEQUERY')

    # sending from denied requester and not expecting any response
    srv_msg.send_wait_for_message("MUST", None, expect_response=False)

    # Building lease query message to ask for mac address
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(CIADDR)')
    srv_msg.client_sets_value('Client', 'ciaddr', 0)
    srv_msg.client_sets_value('Client', 'chaddr', "1a:1b:1c:1d:1e:1f")
    srv_msg.client_send_msg('LEASEQUERY')

    # sending from denied requester and not expecting any response
    srv_msg.send_wait_for_message("MUST", None, expect_response=False)

    # Building lease query message to ask for client-id
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(CIADDR)')
    srv_msg.client_sets_value('Client', 'ciaddr', 0)
    srv_msg.client_sets_value('Client', 'htype', 0)
    srv_msg.client_sets_value('Client', 'chaddr', "00")
    srv_msg.client_sets_value('Client', 'hlen', 0)
    srv_msg.client_does_include_with_value('client_id', '00010203040506')
    srv_msg.client_send_msg('LEASEQUERY')

    # sending from denied requester and not expecting any response
    srv_msg.send_wait_for_message("MUST", None, expect_response=False)

    # Building lease query message to ask for ip-address from permitted address to
    # make sure server works correctly.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', '$(MGMT_ADDRESS)')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.1')
    srv_msg.client_sets_value('Client', 'htype', 0)
    srv_msg.client_sets_value('Client', 'chaddr', "00")
    srv_msg.client_sets_value('Client', 'hlen', 0)
    srv_msg.client_send_msg('LEASEQUERY')

    # sending and testing the response to allowed requester
    srv_msg.send_wait_for_message('MUST', 'LEASEUNASSIGNED')
    srv_msg.response_check_content('ciaddr', '192.168.50.1')
    srv_msg.response_check_include_option(53)
    srv_msg.response_check_option_content(53, 'value', 11)
