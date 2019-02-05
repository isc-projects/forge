"""DHCPv6 Moving Client"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import misc
from features import srv_msg


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.movingclient
def test_v6_movingclient_0(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::10')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:3::/64',
                                                       '2001:db8:3::1-2001:db8:3::10')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '1000')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8:1::1000')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '1000')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8:2::1000')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '1000')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'abcd')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8:3::1000')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.movingclient
def test_v6_movingclient_1(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::10')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '1000')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8:1::1000')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '1000')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'CONFIRM')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8:2::2000')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    # Relayed Message MUST include option 3.
    # Relayed Message option 3 MUST NOT contain sub-option 5.
    # Relayed Message option 3 MUST contain sub-option 13.
    # Relayed Message sub-option 13 from option 3 MUST contain statuscode 2.


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.movingclient
def test_v6_movingclient_2(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::10')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '1000')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8:1::1000')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '1000')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REBIND')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8:2::2000')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')
    # Response option 3 MUST contain sub-option 5.
    # Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
    # Response sub-option 5 from option 3 MUST contain validlft 4000.
    # Response sub-option 5 from option 3 MUST contain address 3000::1.
    # Response sub-option 5 from option 3 MUST contain validlft 0.


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.movingclient
def test_v6_movingclient_3(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::10')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '1000')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.client_save_option(step, 'server-id')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8:1::1000')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '1000')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RELEASE')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8:2::2000')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')

    # Response MUST include option 3.
    # Response option 3 MUST contain T1 0.
    # Response option 3 MUST contain T2 0.
    # Response option 3 MUST contain sub-option 13.
    # Response sub-option 13 from option 3 MUST contain statuscode 0.
    # Response MUST include option 13.
    # Response option 13 MUST contain statuscode 0.


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.movingclient
def test_v6_movingclient_4(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ff')
    srv_control.config_srv_another_subnet_no_interface(step,
                                                       '2001:db8:2::/64',
                                                       '2001:db8:2::1-2001:db8:2::10')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '1000')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.client_save_option(step, 'server-id')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'xyz')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8:1::1000')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '1000')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RENEW')

    srv_msg.client_sets_value(step, 'RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include(step, 'RelayAgent', None, 'interface-id')
    srv_msg.client_sets_value(step, 'RelayAgent', 'linkaddr', '2001:db8:2::2000')
    srv_msg.create_relay_forward(step, '1', None)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'RELAYREPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '9')
    srv_msg.response_check_option_content(step, 'Response', '9', None, 'Relayed', 'Message')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '1')
    srv_msg.response_check_include_option(step, 'Relayed Message', None, '2')

    # Response MUST include option 3.
    # Response option 3 MUST contain sub-option 5.
