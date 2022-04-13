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
        srv_control.add_parameter_to_hook(1, "hostname-expr", "" if hostname == 'empty' else  "'host-'+hexstring(option[1].hex, '-')")
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
