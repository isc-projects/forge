"""ISC_DHCP DHCPv6 Keywords fixed-address6"""


import sys
if 'features' not in sys.path:
    sys.path.append('features')

if 'pytest' in sys.argv[0]:
    import pytest
else:
    import lettuce as pytest

import misc
import srv_control
import srv_msg


@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.fixed_address6
def test_v6_dhcpd_keyword_fixed_address6(step):
    """new-v6.dhcpd.keyword.fixed-address6"""
    # #
    # # Tests address assignment when fixed-address6 is used.
    # #
    # # Server is configured with one subnet 3000::/64, with one pool of two
    # # addresses 3000::1 - 3000::2.  One address, 3000::1, is reserved to a
    # # specific client (DUID2) using the host statement and fixed-address6.
    # #
    # # Stage 1: Client with DUID1 asks for and should be granted 3000::2,
    # # the only address available to Clients who are NOT DUID2
    # #
    # # Stage 2: Client with DUID3 solicts an address but should be denied
    # #
    # # Stage 3: Client with DUID2 solicits and should be should be granted
    # # 3000::1, the reserved address.
    # #
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.run_command(step, 'host specialclient {')
    srv_control.run_command(step,
                            '  host-identifier option dhcp6.client-id 00:03:00:01:ff:ff:ff:ff:ff:02;')
    srv_control.run_command(step, '  fixed-address6 3000::1; }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # Stage 1: DUID1 asks for an address

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    # Server should offer 3000::2

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::2')

    # DUID1 accepts the address

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_send_msg(step, 'CONFIRM')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')

    # Stage 2: DUID3 asks for an address

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    # Server should response with NoAddrAvail

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '2')

    # Stage 3: DUID2 asks for an address

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    # Server should offer the reserved address, 3000::1

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_send_msg(step, 'CONFIRM')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')


