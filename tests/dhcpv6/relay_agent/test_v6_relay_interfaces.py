"""DHCPv6 Relay Agent"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import misc
import srv_msg
import references
from forge_cfg import world


@pytest.mark.v6
@pytest.mark.relay
@pytest.mark.kea_only
def test_v6_relay_interface_local_and_relay_interface_in_the_same_subnet():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    world.dhcp_cfg["subnet6"][0].update({"interface-id": "abc",
                                         "interface": '$(SERVER_IFACE)',
                                         "relay": {"ip-address": "3000::1005"}})
    srv_control.build_and_send_config_files()
    srv_control.start_srv_during_process('DHCP', 'configuration')

    references.references_check('Kea')


@pytest.mark.v6
@pytest.mark.relay
@pytest.mark.kea_only
def test_v6_relay_interface_two_subnets():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    srv_control.set_conf_parameter_subnet('interface-id', 'abc', 0)
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::10')
    srv_control.set_conf_parameter_subnet('interface-id', 'xyz', 1)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:2::1')

    references.references_check('Kea')


@pytest.mark.v6
@pytest.mark.relay
@pytest.mark.kea_only
def test_v6_relay_relayaddress_two_subnets():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    srv_control.add_line_to_subnet(0, {"relay": {"ip-address": "3000::1005"}})
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::10')
    srv_control.add_line_to_subnet(1, {"relay": {"ip-address": "3000::2005"}})
    srv_control.set_conf_parameter_subnet('interface-id', 'xyz', 1)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '3000::1005')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '3000::2005')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:2::1')

    references.references_check('Kea')


@pytest.mark.v6
@pytest.mark.relay
@pytest.mark.kea_only
@pytest.mark.disabled
def test_v6_relay_relayaddress_interface_id_just_one_matching():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    srv_control.set_conf_parameter_subnet('interface-id', 'xyz', 0)
    srv_control.add_line_to_subnet(0, {"relay": {"ip-address": "3000::1005"}})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '3000::3005')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5, expect_include=False)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


@pytest.mark.v6
@pytest.mark.relay
@pytest.mark.kea_only
@pytest.mark.disabled
def test_v6_relay_relayaddress_interface_id_just_one_matching_2():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    srv_control.set_conf_parameter_subnet('interface-id', 'xyz', 0)
    srv_control.add_line_to_subnet(0, {"relay": {"ip-address": "3000::1005"}})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '3000::1005')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5, expect_include=False)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


@pytest.mark.v6
@pytest.mark.relay
@pytest.mark.kea_only
@pytest.mark.disabled
def test_v6_relay_relayaddress_interface_id_just_one_matching_3():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    srv_control.set_conf_parameter_subnet('interface-id', 'xyz', 0)
    srv_control.add_line_to_subnet(0, {"relay": {"ip-address": "3000::1005"}})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:1::1000')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5, expect_include=False)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


@pytest.mark.v6
@pytest.mark.relay
@pytest.mark.kea_only
def test_v6_relay_relayaddress_interface_id_two_subnets():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    srv_control.set_conf_parameter_subnet('interface-id', 'xyz', 0)
    srv_control.add_line_to_subnet(0, {"relay": {"ip-address": "3000::1005"}})
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::10')
    srv_control.set_conf_parameter_subnet('interface-id', 'abc', 1)
    srv_control.add_line_to_subnet(1, {"relay": {"ip-address": "3000::1005"}})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '3000::1005')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '3000::1005')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:2::1')

    references.references_check('Kea')


@pytest.mark.v6
@pytest.mark.relay
@pytest.mark.kea_only
def test_v6_relay_relayaddress_interface_id_two_subnets_2():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    srv_control.set_conf_parameter_subnet('interface-id', 'xyz', 0)
    srv_control.add_line_to_subnet(0, {"relay": {"ip-address": "3000::2005"}})
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::10')
    srv_control.set_conf_parameter_subnet('interface-id', 'abc', 1)
    srv_control.add_line_to_subnet(1, {"relay": {"ip-address": "3000::1005"}})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '3000::2005')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '3000::1005')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:2::1')

    references.references_check('Kea')


@pytest.mark.v6
@pytest.mark.relay
@pytest.mark.kea_only
def test_v6_relay_relayaddress_not_matching():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    srv_control.add_line_to_subnet(0, {"relay": {"ip-address": "3000::2005"}})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:2::100')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)


@pytest.mark.v6
@pytest.mark.relay
@pytest.mark.kea_only
def test_v6_relay_relayaddress_within_subnet():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    srv_control.add_line_to_subnet(0, {"relay": {"ip-address": "3000::2005"}})
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', '2001:db8:1::100')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.relay
@pytest.mark.kea_only
def test_v6_relay_interface_one_subnet_not_matching_id():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::10')
    srv_control.set_conf_parameter_subnet('interface-id', 'xyz', 0)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    references.references_check('Kea')


@pytest.mark.v6
@pytest.mark.relay
@pytest.mark.kea_only
def test_v6_relay_interface_two_subnets_direct_client():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.set_conf_parameter_subnet('interface-id', 'abc', 0)
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::10')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'xyz')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1', expect_include=False)

    references.references_check('Kea')


@pytest.mark.v6
@pytest.mark.relay
@pytest.mark.kea_only
def test_v6_relay_interface_two_subnets_same_interface_id():

    misc.test_setup()
    # that is basically misconfiguration!
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.set_conf_parameter_subnet('interface-id', 'abc', 0)
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       '2001:db8:2::11-2001:db8:2::20')
    srv_control.set_conf_parameter_subnet('interface-id', 'abc', 1)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    #  just saving server-id - start
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_save_option('server-id')
    #  just saving server-id - end

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value('Client', 'IA_Address', '2001:db8:1::1')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_add_saved_option()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:33:22:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)

    references.references_check('Kea')
