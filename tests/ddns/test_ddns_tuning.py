# Copyright (C) 2013-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""DDNS Tuning Hook basic tests"""

# pylint: disable=invalid-name,line-too-long

import pytest
from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world


def _get_address(duid, fqdn):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    if fqdn is not None:
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hostname', ['basic', 'suffix', 'empty'])
def test_ddns_tuning_basic(backend, dhcp_version, hostname):
    """
    Test of the "ddns-tuning" premium hook basic functionality.
    This basic test sets ddns-tuning hook parameter to replace hostname with expression including text and hardware address.
    DORA/SARR exchange acquires lease and leaseX-get command returns hostname applied to lease.
    We then compare returned lease with expected.
    Parameter 'suffix' and 'empty' check for proper behaviour with global suffix applied or global tuning disabled.
    """
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)

    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::21')

    srv_control.add_hooks('libdhcp_ddns_tuning.so')
    if dhcp_version == 'v4':
        srv_control.add_parameter_to_hook(1, "hostname-expr", "" if hostname == 'empty' else "'host-'+hexstring(pkt4.mac,'-')")
    else:
        srv_control.add_parameter_to_hook(1, "hostname-expr", "" if hostname == 'empty' else "'host-'+hexstring(option[1].hex, '-')")
    srv_control.add_hooks('libdhcp_lease_cmds.so')

    if hostname == 'suffix':
        world.dhcp_cfg['ddns-qualifying-suffix'] = 'foo.bar'

    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.1', fqdn='test.com')
        cmd = {"command": "lease4-get-all"}
        response = srv_msg.send_ctrl_cmd(cmd, 'http')
        if hostname == 'basic':
            assert response['arguments']['leases'][0]['hostname'] == 'host-ff-01-02-03-ff-04'
        elif hostname == 'suffix':
            assert response['arguments']['leases'][0]['hostname'] == 'host-ff-01-02-03-ff-04.foo.bar'
        elif hostname == 'empty':
            assert response['arguments']['leases'][0]['hostname'] == 'test.com.'
    else:
        _get_address(duid='00:03:00:01:66:55:44:33:22:11', fqdn='test.com')
        cmd = {"command": "lease6-get-all"}
        response = srv_msg.send_ctrl_cmd(cmd, 'http')
        if hostname == 'basic':
            assert response['arguments']['leases'][0]['hostname'] == 'host-00-03-00-01-66-55-44-33-22-11.'
        elif hostname == 'suffix':
            assert response['arguments']['leases'][0]['hostname'] == 'host-00-03-00-01-66-55-44-33-22-11.foo.bar.'
        elif hostname == 'empty':
            assert response['arguments']['leases'][0]['hostname'] == 'test.com.'


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hostname', ['basic', 'suffix', 'empty'])
def test_v4_ddns_tuning_subnets(backend, hostname):
    """
    Test of the "ddns-tuning" premium hook basic functionality with configured subnets in IP v4.
    This test sets ddns-tuning hook parameter to replace hostname with expression including text and hardware address
    globally and per subnet.
    First subnet uses global expression, and rest uses respective subnet configured expressions.
    DORA exchange acquires lease and lease4-get command returns hostname applied to lease.
    We then compare returned lease with expected.
    Parameter 'suffix' and 'empty' check for proper behaviour with global suffix applied or global tuning disabled.
    """
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)

    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.10-192.168.51.10')
    srv_control.config_srv_another_subnet_no_interface('192.168.52.0/24', '192.168.52.10-192.168.52.10')
    srv_control.add_line_to_subnet(1, {"user-context": {
            "ddns-tuning": {
                "hostname-expr": "" if hostname == 'empty' else "'host1-'+hexstring(pkt4.mac,'-')"
            }}})
    srv_control.add_line_to_subnet(2, {"user-context": {
            "ddns-tuning": {
                "hostname-expr": "" if hostname == 'empty' else "'host2-'+hexstring(pkt4.mac,'-')"
            }}})
    srv_control.add_hooks('libdhcp_ddns_tuning.so')

    srv_control.add_parameter_to_hook(1, "hostname-expr", "" if hostname == 'empty' else "'host0-'+hexstring(pkt4.mac,'-')")

    srv_control.add_hooks('libdhcp_lease_cmds.so')

    if hostname == 'suffix':
        world.dhcp_cfg['ddns-qualifying-suffix'] = 'foo.bar'

    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.shared_subnet('192.168.52.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    for i in range(3):
        srv_msg.DORA(f'192.168.5{i}.10', chaddr=f'ff:01:02:03:ff:0{i}', fqdn=f'test{i}.com')

    for i in range(3):
        cmd = {"command": "lease4-get",
               "arguments": {"ip-address": f'192.168.5{i}.10'}}
        response = srv_msg.send_ctrl_cmd(cmd, 'http')
        if hostname == 'basic':
            assert response['arguments']['hostname'] == f'host{i}-ff-01-02-03-ff-0{i}'
        elif hostname == 'suffix':
            assert response['arguments']['hostname'] == f'host{i}-ff-01-02-03-ff-0{i}.foo.bar'
        elif hostname == 'empty':
            assert response['arguments']['hostname'] == f'test{i}.com.'


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('hostname', ['basic', 'suffix', 'empty'])
def test_v6_ddns_tuning_subnets(backend, hostname):
    """
    Test of the "ddns-tuning" premium hook basic functionality with configured subnets in IP v6.
    This test sets ddns-tuning hook parameter to replace hostname with expression including text and hardware address
    globally and per subnet.
    First subnet uses global expression, and rest uses respective subnet configured expressions.
    SARR exchange acquires lease and leas6-get command returns hostname applied to lease.
    We then compare returned lease with expected.
    Parameter 'suffix' and 'empty' check for proper behaviour with global suffix applied or global tuning disabled.
    """
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)

    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64', '2001:db8:2::1-2001:db8:2::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:3::/64', '2001:db8:3::1-2001:db8:3::1')
    srv_control.add_line_to_subnet(1, {"user-context": {
            "ddns-tuning": {
                "hostname-expr": "" if hostname == 'empty' else "'host2-'+hexstring(option[1].hex, '-')"
            }}})
    srv_control.add_line_to_subnet(2, {"user-context": {
            "ddns-tuning": {
                "hostname-expr": "" if hostname == 'empty' else "'host3-'+hexstring(option[1].hex, '-')"
            }}})
    srv_control.add_hooks('libdhcp_ddns_tuning.so')

    srv_control.add_parameter_to_hook(1, "hostname-expr", "" if hostname == 'empty' else "'host1-'+hexstring(option[1].hex, '-')")

    srv_control.add_hooks('libdhcp_lease_cmds.so')

    if hostname == 'suffix':
        world.dhcp_cfg['ddns-qualifying-suffix'] = 'foo.bar'

    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    srv_control.shared_subnet('2001:db8:1::/64', 0)
    srv_control.shared_subnet('2001:db8:2::/64', 0)
    srv_control.shared_subnet('2001:db8:3::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    for i in range(1, 4):
        _get_address(duid=f'00:03:00:01:66:55:44:33:22:1{i}', fqdn=f'test{i}.com')

    for i in range(1, 4):
        cmd = {"command": "lease6-get",
               "arguments": {"ip-address": f'2001:db8:{i}::1'}}
        response = srv_msg.send_ctrl_cmd(cmd, 'http')
        if hostname == 'basic':
            assert response['arguments']['hostname'] == f'host{i}-00-03-00-01-66-55-44-33-22-1{i}.'
        elif hostname == 'suffix':
            assert response['arguments']['hostname'] == f'host{i}-00-03-00-01-66-55-44-33-22-1{i}.foo.bar.'
        elif hostname == 'empty':
            assert response['arguments']['hostname'] == f'test{i}.com.'
