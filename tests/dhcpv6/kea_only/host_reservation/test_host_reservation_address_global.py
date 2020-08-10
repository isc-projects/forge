"""Host Reservation DHCPv6"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import srv_msg
import misc

from forge_cfg import world


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_subnet_selection_based_on_global_reservation_of_class():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:b::/64',
                                                       '2001:db8:b::1-2001:db8:b::1')

    world.dhcp_cfg["subnet6"][0]["client-class"] = "NOTspecial"
    world.dhcp_cfg["subnet6"][1]["client-class"] = "special"

    world.dhcp_cfg.update({
        "reservations": [
            {
                "client-classes": [
                    "special"
                ],
                "hw-address": "01:02:03:04:05:07"
            }
        ], "client-classes": [
            {
                "name": "special"
            },
            {
                "name": "NOTspecial",
                "test": "not member('special')"
            }
        ], "reservation-mode": "global"})

    world.dhcp_cfg["subnet6"][1].update({"reservations": [
        {
            "ip-addresses": ["2001:db8:a::1111"],
            "hw-address": "01:02:03:04:05:07"
        }
    ], "reservation-mode": "all"})

    srv_control.shared_subnet('2001:db8:a::/64', 0)
    srv_control.shared_subnet('2001:db8:b::/64', 0)

    srv_control.set_conf_parameter_shared_subnet('name', 'name-abc', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '$(SERVER_IFACE)', 0)

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:01:02:03:04:05:07')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:01:02:03:04:05:07')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, 3)
    srv_msg.response_check_option_content('Response', 3, None, 'sub-option', 5)
    srv_msg.response_check_suboption_content('Response', 5, 3, None, 'addr', '2001:db8:a::1111')


@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.kea_only
def test_v6_pool_selection_based_on_global_reservation_of_class():
    misc.test_setup()
    # pool selection based on global reservation with class
    # address assigned based on reservation on subnet level
    srv_control.config_srv_subnet('2001:db8:1::/64', "2001:db8:1::1-2001:db8:1::1")
    srv_control.new_pool('2001:db8:1::5-2001:db8:1::5', 0)
    world.dhcp_cfg.update({
        "reservations": [
            {
                "client-classes": [
                    "special"
                ],
                "hw-address": "01:02:03:04:05:07"
            }
        ], "client-classes": [
            {
                "name": "special"
            },
            {
                "name": "NOTspecial",
                "test": "not member('special')"
            }

        ], "reservation-mode": "global"})

    world.dhcp_cfg["subnet6"][0]["pools"][0]["client-class"] = "NOTspecial"
    world.dhcp_cfg["subnet6"][0]["pools"][1]["client-class"] = "special"

    world.dhcp_cfg["subnet6"][0].update({"reservations": [
        {
            "ip-addresses": ["2001:db8:1::100"],
            "hw-address": "01:02:03:04:05:07"
        }
    ], "reservation-mode": "all"})

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:01:02:03:04:05:07')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:01:02:03:04:05:07')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, 3)
    srv_msg.response_check_option_content('Response', 3, None, 'sub-option', 5)
    srv_msg.response_check_suboption_content('Response', 5, 3, None, 'addr', "2001:db8:1::100")
