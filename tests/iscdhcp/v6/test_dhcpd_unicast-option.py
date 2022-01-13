"""ISC_DHCP DHCPv6 feature unicast"""

# pylint: disable=invalid-name,line-too-long

import pytest
import misc
import srv_control
import srv_msg

from softwaresupport.isc_dhcp6_server.functions import add_line_in_global


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_feature_unicast_option_defined():
    """new-dhcpd.feature.unicast-option.defined"""
    # Tests that REQUEST, RENEW, RELEASE, and DECLINE can be sent
    # unicast when unicast option is defined.
    #
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address
    # Step 3: Client RENEWs advertised address via unicast
    # - server should reply (grant) the address
    # Step 4: Client RELEASEs granted address via unicast
    # - server should reply with success status code
    # Step 5: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # Step 6: Client declines offered  address via unicast
    # - server should reply with success status code
    #
    misc.test_setup()
    add_line_in_global('ddns-updates off;')
    add_line_in_global('option dhcp6.unicast 3000::;')
    add_line_in_global('authoritative;')
    add_line_in_global('subnet6 3000::/16 {')
    add_line_in_global(' pool6 {')
    add_line_in_global('  range6 3000:: 3000::1;')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # ##############################################################
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # ##############################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(12)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_include_option(12)

    # ##############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address
    # ##############################################################
    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    # ##############################################################
    # Step 3: Client RENEWs advertised address via unicast
    # - server should reply (renew) the address
    # ##############################################################
    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    # ##############################################################
    # Step 4: Client RELEASEs granted address via unicast
    # - server should reply with success status code
    # ##############################################################
    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 0)

    # ##############################################################
    # Step 5: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # ##############################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(12)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_include_option(12)

    # ##############################################################
    # Step 6: Client declines offered  address via unicast
    # - server should reply with success status code
    # ##############################################################
    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 0)

    # ###############################################################################


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_feature_unicast_option_not_defined():
    """new-dhcpd.feature.unicast-option.not_defined"""
    # Tests that REQUEST, RENEW, RELEASE, and DECLINE sent via unicast are
    # rejected when the dhcp6.unicast option is NOT defined.
    #
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address without unicast option
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reject with status code of 5
    # Step 3: Client RENEWs advertised address via unicast
    # - server should reject with status code of 5
    # Step 4: Client RELEASEs granted address via unicast
    # - server should reject with status code of 5
    # Step 5: Client SOLICITs requesting unicast option
    # - server should advertise an address without unicast option
    # Step 6: Client declines offered  address via unicast
    # - server should reject with status code of 5
    #
    misc.test_setup()
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('subnet6 3000::/16 {')
    add_line_in_global(' pool6 {')
    add_line_in_global('  range6 3000:: 3000::1;')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # ##############################################################
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # ##############################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(12)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_include_option(12, expect_include=False)
    srv_msg.client_save_option_count(1, 'IA_NA')
    srv_msg.client_save_option_count(1, 'client-id')
    srv_msg.client_save_option_count(1, 'server-id')

    # ##############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply with status code = 5
    # ##############################################################
    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    # Client adds saved options in set no. 1. and DONT Erase.
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3, expect_include=False)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 5)

    # ##############################################################
    # Step 3: Client RENEWs advertised address via unicast
    # - server should reply with status code = 5
    # ##############################################################
    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    # Client adds saved options in set no. 1. and DONT Erase.
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3, expect_include=False)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 5)

    # ##############################################################
    # Step 4: Client RELEASEs granted address via unicast
    # - server should reply with status code = 5
    # ##############################################################
    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    # Client adds saved options in set no. 1. and DONT Erase.
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 5)

    # ##############################################################
    # Step 5: Client SOLICITs requesting unicast option
    # - server should advertise an address without unicast option
    # ##############################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(12)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_include_option(12, expect_include=False)

    # ##############################################################
    # Step 6: Client declines offered address via unicast
    # - server should reply with status code = 5
    # ##############################################################
    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 5)

    # ###############################################################################


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_feature_unicast_option_defined_subnet():
    """new-dhcpd.feature.unicast-option.defined.subnet"""
    # Tests that IA_NA REQUEST can be sent unicast when unicast option is
    # defined for the subnet.
    #
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    #
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address

    misc.test_setup()
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('subnet6 3000::/16 {')
    add_line_in_global('  option dhcp6.unicast 3000::;')
    add_line_in_global('  pool6 {')
    add_line_in_global('    range6 3000:: 3000::1;')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # ##############################################################
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # ##############################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(12)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_include_option(12)

    # ##############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address
    # ##############################################################
    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    # ###############################################################################


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_feature_unicast_option_defined_shared_network():
    """new-dhcpd.feature.unicast-option.defined.shared-network"""
    # Tests that IA_NA REQUEST can be sent unicast when unicast option is
    # defined for the shared-subnet.
    #
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    #
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address

    misc.test_setup()
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('shared-network net1 {')
    add_line_in_global('    option dhcp6.unicast 3000::;')
    add_line_in_global('    subnet6 3000::/16 {')
    add_line_in_global('    pool6 {')
    add_line_in_global('      range6 3000:: 3000::1;')
    add_line_in_global('    }')
    add_line_in_global('  }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # ##############################################################
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # ##############################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(12)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_include_option(12)

    # ##############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address
    # ##############################################################
    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    # ###############################################################################


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_feature_unicast_option_defined_IA_PD():
    """new-dhcpd.feature.unicast-option.defined.IA_PD"""
    # Tests that IA_PD REQUEST can be sent unicast when unicast option is
    # defined.
    #
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    #
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address

    misc.test_setup()
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('subnet6 3000::/64 {')
    add_line_in_global('  option dhcp6.unicast 3000::;')
    add_line_in_global('  pool6 {')
    add_line_in_global('    prefix6 3000:0:0:0:100:: 3000:0:0:0:0200:: /80;')
    add_line_in_global('  }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # ##############################################################
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # ##############################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 0)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    # ##############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address
    # ##############################################################
    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_option_content(25, 'sub-option', 26)

    # ###############################################################################


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_feature_unicast_option_defined_IA_TA():
    """new-dhcpd.feature.unicast-option.defined.IA_TA"""
    # Tests that IA_TA REQUEST can be sent unicast when unicast option is
    # defined.
    #
    # ##################################################################
    # ##################################################################
    #
    # @TODO  THIS TEST WILL FAIL UNTIL FORGE SUPPORTS IA_TA
    #
    # ##################################################################
    # ##################################################################
    #
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    #
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address

    misc.test_setup()
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('subnet6 3000::/64 {')
    add_line_in_global('  option dhcp6.unicast 3000::;')
    add_line_in_global('  pool6 {')
    add_line_in_global('      range6 3000:: temporary;')
    add_line_in_global('  }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # ##############################################################
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # ##############################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_TA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_include_option(12)

    # ##############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address
    # ##############################################################
    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_copy_option('IA_TA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(4)
    srv_msg.response_check_option_content(4, 'sub-option', 5)
