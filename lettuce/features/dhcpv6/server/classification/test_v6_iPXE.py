"""DHCPv6 iPXE boot tests"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import misc


@pytest.mark.v6
@pytest.mark.iPXE
def test_v6_IPXE_1(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8::/64', '$(EMPTY)')
    srv_control.create_new_class(step, 'a-ipxe')
    srv_control.add_test_to_class(step, '1', 'test', 'substring(option[15].hex,2,4) == \'iPXE\'')
    srv_control.add_option_to_defined_class(step,
                                            '1',
                                            'bootfile-url',
                                            'http://[2001:db8::1]/ubuntu.cfg')
    # Server is configured with client-classification option in subnet 0 with name a-ipxe.
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'archtypes', '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-arch-type')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_sets_value(step, 'Client', 'user_class_data', 'iPXE')
    srv_msg.client_does_include(step, 'Client', None, 'user-class')
    srv_msg.client_requests_option(step, '59')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '59')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '59',
                                          None,
                                          'optdata',
                                          'http://[2001:db8::1]/ubuntu.cfg')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '2')


@pytest.mark.v6
@pytest.mark.iPXE
def test_v6_IPXE_2(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8::/64', '$(EMPTY)')
    srv_control.create_new_class(step, 'a-ipxe')
    srv_control.add_test_to_class(step, '1', 'test', 'option[61].hex == 0x0007')
    srv_control.add_option_to_defined_class(step,
                                            '1',
                                            'bootfile-url',
                                            'http://[2001:db8::1]/ipxe.efi')
    # Server is configured with client-classification option in subnet 0 with name a-ipxe.
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'archtypes', '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-arch-type')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '59')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '59')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '59',
                                          None,
                                          'optdata',
                                          'http://[2001:db8::1]/ipxe.efi')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '2')


@pytest.mark.v6
@pytest.mark.iPXE
def test_v6_IPXE_combined(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8::/64', '$(EMPTY)')

    srv_control.create_new_class(step, 'a-ipxe')
    srv_control.add_test_to_class(step, '1', 'test', 'substring(option[15].hex,2,4) == \'iPXE\'')
    srv_control.add_option_to_defined_class(step,
                                            '1',
                                            'bootfile-url',
                                            'http://[2001:db8::1]/ubuntu.cfg')

    srv_control.create_new_class(step, 'b-ipxe')
    srv_control.add_test_to_class(step, '2', 'test', 'option[61].hex == 0x0007')
    srv_control.add_option_to_defined_class(step,
                                            '2',
                                            'bootfile-url',
                                            'http://[2001:db8::1]/ipxe.efi')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'archtypes', '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-arch-type')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_requests_option(step, '59')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '59')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '59',
                                          None,
                                          'optdata',
                                          'http://[2001:db8::1]/ipxe.efi')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '2')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'archtypes', '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-arch-type')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_sets_value(step, 'Client', 'user_class_data', 'iPXE')
    srv_msg.client_does_include(step, 'Client', None, 'user-class')
    srv_msg.client_requests_option(step, '59')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '59')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '59',
                                          None,
                                          'optdata',
                                          'http://[2001:db8::1]/ubuntu.cfg')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '2')
