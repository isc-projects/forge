""" DHCPv6 options defined in subnet"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import srv_control
import misc

from forge_cfg import world


def _get_lease(duid, pref_val):
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_requests_option(7)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(7)
    srv_msg.response_check_option_content(7, 'prefval', pref_val)


@pytest.mark.v6
@pytest.mark.options
@pytest.mark.preference
def test_v6_options_pool_level():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.new_pool("2001:db8:1::500-2001:db8:1::500", 0)
    srv_control.config_srv_opt('preference', "20")

    option = {"name": "preference", "space": "dhcp6", "data": "1"}
    world.dhcp_cfg["subnet6"][0]["pools"][0].update({"option-data": [option]})

    option2 = {"name": "preference", "space": "dhcp6", "data": "2"}
    world.dhcp_cfg["subnet6"][0]["pools"][1].update({"option-data": [option2]})

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # lease from first pool should have preference val set to 1
    _get_lease('00:03:00:01:ff:ff:ff:ff:ff:01', 1)
    # lease from seconnd pool should have preference val set to 2
    _get_lease('00:03:00:01:ff:ff:ff:ff:ff:02', 2)


