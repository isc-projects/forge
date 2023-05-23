# Copyright (C) 2013-2023 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""DHCPv4 and DHCPv6 leasequery tests"""

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
    srv_control.add_parameter_to_hook('libdhcp_lease_query.so', {"requesters": ["$(CIADDR)"]})
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
    srv_msg.response_check_option_content(82, 'value', "0106060106020603")
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
    srv_control.add_parameter_to_hook('libdhcp_lease_query.so', {"requesters": ["$(CIADDR)"]})
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
    srv_msg.response_check_option_content(82, 'value', "0106060106020603")
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
    srv_control.add_parameter_to_hook('libdhcp_lease_query.so', {"requesters": ["$(CIADDR)"]})
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
    srv_msg.response_check_option_content(82, 'value', "0106060106020603")
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
    srv_control.add_parameter_to_hook('libdhcp_lease_query.so', {"requesters": [world.f_cfg.mgmt_address]})
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


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile'])
def test_v6_negative(backend):
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::2')
    srv_control.config_srv_prefix('2001:db8:3::', 0, 126, 128)
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # adding hook and required parameters
    srv_control.add_hooks('libdhcp_lease_query.so')
    # Set permitted requester to forge machine ip
    srv_control.add_parameter_to_hook('libdhcp_lease_query.so', {"requesters": [world.f_cfg.cli_link_local]})
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    # missing client-id
    srv_msg.client_sets_value('Client', 'lq-query-type', 2)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")
    srv_msg.client_does_include('Client', 'lq-query')
    # srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('LEASEQUERY')
    srv_msg.send_wait_for_message('MUST', None, expect_response=False)
    # reason: DHCPV6_LEASEQUERY must supply a D6O_CLIENTID

    # incorrect server-id
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_sets_value('Client', 'lq-query-type', 2)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'server_id', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'server-id')
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', None, expect_response=False)
    # unknown server-id: type=00002, len=00010: 00:03:00:01:ff:ff:ff:ff:ff:01

    # missing lq-query-options
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', None, expect_response=False)
    # reason: DHCPV6_LEASEQUERY must supply a D6O_LQ_QUERY option

    # wrong query id
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_sets_value('Client', 'lq-query-type', 7)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lq-query option
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lease-query message
    srv_msg.client_send_msg('LEASEQUERY')

    # sending and testing the response to allowed requester
    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 7)  # rfc5007 section 4.1.3.

    # wrong query id
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_sets_value('Client', 'lq-query-type', 4)  # this type is for BULK leasequery
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lq-query option
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lease-query message
    srv_msg.client_send_msg('LEASEQUERY')

    # sending and testing the response to allowed requester
    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 7)  # rfc5007 section 4.1.3.

    # non existing lease by duid
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_sets_value('Client', 'lq-query-type', 2)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lq-query option
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lease-query message
    srv_msg.client_send_msg('LEASEQUERY')

    # sending and testing the response to allowed requester
    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    opt = srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 0)
    assert opt.statusmsg == b'no active leases', "Status code option include incorrect message"
    srv_msg.response_check_include_option(45, expect_include=False)
    srv_msg.response_check_include_option(48, expect_include=False)

    # non existing lease by link
    srv_msg.client_sets_value('Client', 'lq-query-type', 1)
    srv_msg.client_sets_value('Client', 'lq-query-address', "3000::1")

    srv_msg.client_sets_value('Client', 'IA_Address', '2001:db8:1::2')
    srv_msg.client_does_include('Client', 'IA_Address')  # this will add option to world.iaad
    # rather to world.cliopts because it not suppose to be used that way
    # let's change it just for this test
    world.cliopts.append(world.iaad[-1])
    world.iaad = []

    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    opt = srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 0)
    srv_msg.response_check_include_option(45, expect_include=False)
    srv_msg.response_check_include_option(48, expect_include=False)

    # missing IA Address in query by address
    srv_msg.client_sets_value('Client', 'lq-query-type', 1)
    srv_msg.client_sets_value('Client', 'lq-query-address', "3000::1")

    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    opt = srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 8)
    srv_msg.response_check_include_option(45, expect_include=False)
    srv_msg.response_check_include_option(48, expect_include=False)

    # missing duid in query by duid
    srv_msg.client_sets_value('Client', 'lq-query-type', 2)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")

    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    opt = srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 8)
    srv_msg.response_check_include_option(45, expect_include=False)
    srv_msg.response_check_include_option(48, expect_include=False)

    # query correct but link is not configured on this server
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_sets_value('Client', 'lq-query-type', 2)
    srv_msg.client_sets_value('Client', 'lq-query-address', "3000::/64")
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('LEASEQUERY')

    # sending and testing the response to allowed requester
    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 9)

    # let's do the same query, but with different address allowed in leasequery configuration
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::2')
    srv_control.config_srv_prefix('2001:db8:3::', 0, 126, 128)
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # adding hook and required parameters
    srv_control.add_hooks('libdhcp_lease_query.so')
    srv_control.add_parameter_to_hook('libdhcp_lease_query.so', {"requesters": ["3300::11"]})
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'restarted')

    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_sets_value('Client', 'lq-query-type', 2)
    srv_msg.client_sets_value('Client', 'lq-query-address', "3000::/64")
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('LEASEQUERY')

    # we shouldn't get response
    srv_msg.send_wait_for_message('MUST', None, expect_response=False)

    # and check if kea is actually working
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_get_leases(backend):
    """
    Test of v6 lease query messages asking for all assigned leases, with request by link and duid
    """

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::2')
    srv_control.config_srv_prefix('2001:db8:3::', 0, 126, 128)
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # adding hook and required parameters
    srv_control.add_hooks('libdhcp_lease_query.so')
    # Set permitted requester to forge machine ip
    srv_control.add_parameter_to_hook('libdhcp_lease_query.so', {"requesters": [world.f_cfg.cli_link_local]})

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # let's add leases with just address
    cmd = {"command": "lease6-add", "arguments": {"subnet-id": 1,
                                                  "ip-address": "2001:db8:1::1",
                                                  "duid": '00:03:00:01:f6:f5:f4:f3:f2:04',
                                                  "iaid": 1234}}
    srv_msg.send_ctrl_cmd(cmd)

    # let's get a lease with an address and prefix
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('IA_PD')

    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    # leasequery type 2 - based on client id should return prefix and address
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_sets_value('Client', 'lq-query-type', 2)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lq-query option
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lease-query message
    srv_msg.client_send_msg('LEASEQUERY')

    # sending and testing the response to allowed requester
    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 0)
    # 45 it's Leasequery option - Client data option, and has suboptions
    srv_msg.response_check_include_option(45)
    srv_msg.response_check_option_content(45, 'sub-option', 1)
    srv_msg.response_check_suboption_content(1, 45, 'duid', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.response_check_option_content(45, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 45, 'addr', "2001:db8:1::2")
    srv_msg.response_check_option_content(45, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 45, 'prefix', "2001:db8:3::")
    srv_msg.response_check_option_content(45, 'sub-option', 46)

    # leasequery type 1 - based on link should return just address
    srv_msg.client_sets_value('Client', 'lq-query-type', 1)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")

    srv_msg.client_sets_value('Client', 'IA_Address', '2001:db8:1::2')
    srv_msg.client_does_include('Client', 'IA_Address')  # this will add option to world.iaad
    # rather to world.cliopts because it not suppose to be used that way
    # let's change it just for this test
    world.cliopts.append(world.iaad[-1])
    world.iaad = []

    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lease-query message
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 0)
    # 45 it's Leasequery option - Client data option, and has suboptions
    srv_msg.response_check_include_option(45)
    srv_msg.response_check_option_content(45, 'sub-option', 1)
    srv_msg.response_check_suboption_content(1, 45, 'duid', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.response_check_option_content(45, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 45, 'addr', "2001:db8:1::2")
    srv_msg.response_check_option_content(45, 'sub-option', 26, expect_include=False)
    srv_msg.response_check_option_content(45, 'sub-option', 46)

    # now let's checked lease that been added via command control channel

    # leasequery type 2 - based on client id should return address
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.client_sets_value('Client', 'lq-query-type', 2)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lq-query option
    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lease-query message
    srv_msg.client_send_msg('LEASEQUERY')

    # sending and testing the response to allowed requester
    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 0)
    # 45 it's Leasequery option - Client data option, and has suboptions
    srv_msg.response_check_include_option(45)
    srv_msg.response_check_option_content(45, 'sub-option', 1)
    srv_msg.response_check_suboption_content(1, 45, 'duid', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.response_check_option_content(45, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 45, 'addr', "2001:db8:1::1")
    srv_msg.response_check_option_content(45, 'sub-option', 26, expect_include=False)
    srv_msg.response_check_option_content(45, 'sub-option', 46)

    # and the same lease via query by link

    # leasequery type 1 - based on link should return just address
    srv_msg.client_sets_value('Client', 'lq-query-type', 1)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")

    srv_msg.client_sets_value('Client', 'IA_Address', '2001:db8:1::1')
    srv_msg.client_does_include('Client', 'IA_Address')  # this will add option to world.iaad
    # rather to world.cliopts because it not suppose to be used that way
    # let's change it just for this test
    world.cliopts.append(world.iaad[-1])
    world.iaad = []

    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 0)
    # 45 it's Leasequery option - Client data option, and has suboptions
    srv_msg.response_check_include_option(45)
    srv_msg.response_check_option_content(45, 'sub-option', 1)
    srv_msg.response_check_suboption_content(1, 45, 'duid', '00:03:00:01:f6:f5:f4:f3:f2:04')
    srv_msg.response_check_option_content(45, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 45, 'addr', "2001:db8:1::1")
    srv_msg.response_check_option_content(45, 'sub-option', 26, expect_include=False)
    srv_msg.response_check_option_content(45, 'sub-option', 46)


def _get_prefix(mac):
    # let's get a lease with an address and prefix
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', f'00:03:00:01:{mac}')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', f'00:03:00:01:{mac}')
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_v6_query_address_get_back_prefix(backend):
    """
    If client asks for address and it wasn't assigned directly, but it was included in a prefix that was delegated
    server should send back this prefix
    """

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::2')
    srv_control.config_srv_prefix('2001:db8:3::', 0, 110, 112)
    world.dhcp_cfg['store-extended-info'] = True
    srv_control.define_temporary_lease_db_backend(backend)
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # adding hook and required parameters
    srv_control.add_hooks('libdhcp_lease_query.so')
    # Set permitted requester to forge machine ip
    srv_control.add_parameter_to_hook('libdhcp_lease_query.so', {"requesters": [world.f_cfg.cli_link_local]})

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    _get_prefix("ff:ff:ff:ff:ff:02")
    _get_prefix("ff:ff:ff:ff:ff:03")
    _get_prefix("ff:ff:ff:ff:ff:04")

    # prefixes assigned 2001:db8:3:: 2001:db8:3::1:0 2001:db8:3::2:0

    # leasequery type 1 - request address but we should get prefix that include this address
    # let's check 2001:db8:3::
    srv_msg.client_sets_value('Client', 'lq-query-type', 1)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")

    srv_msg.client_sets_value('Client', 'IA_Address', '2001:db8:3::1')
    srv_msg.client_does_include('Client', 'IA_Address')  # this will add option to world.iaad
    # rather to world.cliopts because it not suppose to be used that way
    # let's change it just for this test
    world.cliopts.append(world.iaad[-1])
    world.iaad = []

    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lease-query message
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 0)
    # 45 it's Leasequery option - Client data option, and has suboptions
    srv_msg.response_check_include_option(45)
    srv_msg.response_check_option_content(45, 'sub-option', 1)
    srv_msg.response_check_suboption_content(1, 45, 'duid', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.response_check_option_content(45, 'sub-option', 5, expect_include=False)
    srv_msg.response_check_option_content(45, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 45, 'prefix', "2001:db8:3::")
    srv_msg.response_check_suboption_content(26, 45, 'plen', 112)
    srv_msg.response_check_option_content(45, 'sub-option', 46)

    # leasequery type 1 - request address but we should get prefix that include this address
    # let's check 2001:db8:3::1:0
    srv_msg.client_sets_value('Client', 'lq-query-type', 1)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")

    srv_msg.client_sets_value('Client', 'IA_Address', '2001:db8:3::1:1')
    srv_msg.client_does_include('Client', 'IA_Address')  # this will add option to world.iaad
    # rather to world.cliopts because it not suppose to be used that way
    # let's change it just for this test
    world.cliopts.append(world.iaad[-1])
    world.iaad = []

    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lease-query message
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 0)
    srv_msg.response_check_suboption_content(1, 45, 'duid', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.response_check_option_content(45, 'sub-option', 5, expect_include=False)
    srv_msg.response_check_option_content(45, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 45, 'prefix', "2001:db8:3::1:0")
    srv_msg.response_check_suboption_content(26, 45, 'plen', 112)
    srv_msg.response_check_option_content(45, 'sub-option', 46)

    # leasequery type 1 - request address but we should get prefix that include this address
    # let's check 2001:db8:3::2:0
    srv_msg.client_sets_value('Client', 'lq-query-type', 1)
    srv_msg.client_sets_value('Client', 'lq-query-address', "0::0")
    srv_msg.client_sets_value('Client', 'IA_Address', '2001:db8:3::2:1')
    srv_msg.client_does_include('Client', 'IA_Address')  # this will add option to world.iaad
    # rather to world.cliopts because it not suppose to be used that way
    # let's change it just for this test
    world.cliopts.append(world.iaad[-1])
    world.iaad = []

    srv_msg.client_does_include('Client', 'lq-query')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')  # this will be added to lease-query message
    srv_msg.client_send_msg('LEASEQUERY')

    srv_msg.send_wait_for_message('MUST', 'LEASEQUERY-REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 0)
    srv_msg.response_check_suboption_content(1, 45, 'duid', '00:03:00:01:ff:ff:ff:ff:ff:04')
    srv_msg.response_check_option_content(45, 'sub-option', 5, expect_include=False)
    srv_msg.response_check_option_content(45, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 45, 'prefix', "2001:db8:3::2:0")
    srv_msg.response_check_suboption_content(26, 45, 'plen', 112)
    srv_msg.response_check_option_content(45, 'sub-option', 46)
