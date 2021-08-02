"""ISC_DHCP DHCPv6 feature unicast"""


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
@pytest.mark.dhcp6
@pytest.mark.NA
@pytest.mark.rfc3315
@pytest.mark.feature
@pytest.mark.unicast_option
def test_dhcpd_feature_unicast_option_defined(step):
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
    misc.test_setup(step)
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'option dhcp6.unicast 3000::;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'subnet6 3000::/16 {')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  range6 3000:: 3000::1;')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # ##############################################################
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_include_option(step, 'Response', None, '12')

    # ##############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.unicast_addres(step, 'GLOBAL', None)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    # ##############################################################
    # Step 3: Client RENEWs advertised address via unicast
    # - server should reply (renew) the address
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.unicast_addres(step, 'GLOBAL', None)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'RENEW')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    # ##############################################################
    # Step 4: Client RELEASEs granted address via unicast
    # - server should reply with success status code
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.unicast_addres(step, 'GLOBAL', None)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'statuscode', '0')

    # ##############################################################
    # Step 5: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_include_option(step, 'Response', None, '12')

    # ##############################################################
    # Step 6: Client declines offered  address via unicast
    # - server should reply with success status code
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.unicast_addres(step, 'GLOBAL', None)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'DECLINE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'statuscode', '0')

    # ###############################################################################


@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.NA
@pytest.mark.rfc3315
@pytest.mark.feature
@pytest.mark.unicast_option
def test_dhcpd_feature_unicast_option_not_defined(step):
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
    misc.test_setup(step)
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'subnet6 3000::/16 {')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  range6 3000:: 3000::1;')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # ##############################################################
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '12')
    srv_msg.client_save_option_count(step, '1', 'IA_NA')
    srv_msg.client_save_option_count(step, '1', 'client-id')
    srv_msg.client_save_option_count(step, '1', 'server-id')

    # ##############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply with status code = 5
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.unicast_addres(step, 'GLOBAL', None)
    # Client adds saved options in set no. 1. and DONT Erase.
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '3')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'statuscode', '5')

    # ##############################################################
    # Step 3: Client RENEWs advertised address via unicast
    # - server should reply with status code = 5
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.unicast_addres(step, 'GLOBAL', None)
    # Client adds saved options in set no. 1. and DONT Erase.
    srv_msg.client_send_msg(step, 'RENEW')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '3')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'statuscode', '5')

    # ##############################################################
    # Step 4: Client RELEASEs granted address via unicast
    # - server should reply with status code = 5
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.unicast_addres(step, 'GLOBAL', None)
    # Client adds saved options in set no. 1. and DONT Erase.
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'statuscode', '5')

    # ##############################################################
    # Step 5: Client SOLICITs requesting unicast option
    # - server should advertise an address without unicast option
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '12')

    # ##############################################################
    # Step 6: Client declines offered address via unicast
    # - server should reply with status code = 5
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.unicast_addres(step, 'GLOBAL', None)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'DECLINE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'statuscode', '5')

    # ###############################################################################


@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.NA
@pytest.mark.rfc3315
@pytest.mark.feature
@pytest.mark.unicast_option
def test_dhcpd_feature_unicast_option_defined_subnet(step):
    """new-dhcpd.feature.unicast-option.defined.subnet"""
    # Tests that IA_NA REQUEST can be sent unicast when unicast option is
    # defined for the subnet.
    # 
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # 
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address

    misc.test_setup(step)
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'subnet6 3000::/16 {')
    srv_control.run_command(step, '  option dhcp6.unicast 3000::;')
    srv_control.run_command(step, '  pool6 {')
    srv_control.run_command(step, '    range6 3000:: 3000::1;')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # ##############################################################
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_include_option(step, 'Response', None, '12')

    # ##############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.unicast_addres(step, 'GLOBAL', None)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    # ###############################################################################


@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.NA
@pytest.mark.rfc3315
@pytest.mark.feature
@pytest.mark.unicast_option
def test_dhcpd_feature_unicast_option_defined_shared_network(step):
    """new-dhcpd.feature.unicast-option.defined.shared-network"""
    # Tests that IA_NA REQUEST can be sent unicast when unicast option is
    # defined for the shared-subnet.
    # 
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # 
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address

    misc.test_setup(step)
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'shared-network net1 {')
    srv_control.run_command(step, '    option dhcp6.unicast 3000::;')
    srv_control.run_command(step, '    subnet6 3000::/16 {')
    srv_control.run_command(step, '    pool6 {')
    srv_control.run_command(step, '      range6 3000:: 3000::1;')
    srv_control.run_command(step, '    }')
    srv_control.run_command(step, '  }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # ##############################################################
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '12')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_include_option(step, 'Response', None, '12')

    # ##############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.unicast_addres(step, 'GLOBAL', None)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    # ###############################################################################


@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3315
@pytest.mark.feature
@pytest.mark.unicast_option
def test_dhcpd_feature_unicast_option_defined_IA_PD(step):
    """new-dhcpd.feature.unicast-option.defined.IA_PD"""
    # Tests that IA_PD REQUEST can be sent unicast when unicast option is
    # defined.
    # 
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # 
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address

    misc.test_setup(step)
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'subnet6 3000::/64 {')
    srv_control.run_command(step, '  option dhcp6.unicast 3000::;')
    srv_control.run_command(step, '  pool6 {')
    srv_control.run_command(step, '    prefix6 3000:0:0:0:100:: 3000:0:0:0:0200:: /80;')
    srv_control.run_command(step, '  }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # ##############################################################
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '0')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')

    # ##############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.unicast_addres(step, 'GLOBAL', None)
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')

    # ###############################################################################


@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3315
@pytest.mark.feature
@pytest.mark.unicast_option
def test_dhcpd_feature_unicast_option_defined_IA_TA(step):
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

    misc.test_setup(step)
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'subnet6 3000::/64 {')
    srv_control.run_command(step, '  option dhcp6.unicast 3000::;')
    srv_control.run_command(step, '  pool6 {')
    srv_control.run_command(step, '      range6 3000:: temporary;')
    srv_control.run_command(step, '  }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # ##############################################################
    # Step 1: Client SOLICITs requesting unicast option
    # - server should advertise an address and include unicast option
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_TA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_include_option(step, 'Response', None, '12')

    # ##############################################################
    # Step 2: Client REQUESTs advertised address via unicast
    # - server should reply (grant) the address
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.unicast_addres(step, 'GLOBAL', None)
    srv_msg.client_copy_option(step, 'IA_TA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '4')
    srv_msg.response_check_option_content(step, 'Response', '4', None, 'sub-option', '5')


