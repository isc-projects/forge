"""ISC_DHCP DHCPv6 Keywords"""


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
@pytest.mark.ddns
@pytest.mark.forward
def test_v6_dhcpd_keyword_ddns_forward_add(step):
    """new-v6.dhcpd.keyword.ddns.forward.add"""
    # #
    # # Testing: Checks that a forward add is attempted when the configuration
    # # is valid but minimal and client sends a request with valid fqdn
    # #
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/32', '3000::2-3000::2')
    srv_control.run_command(step, 'ddns-updates true;')
    srv_control.run_command(step, 'ddns-domainname "six.example.com";')
    srv_control.run_command(step, 'fqdn-reply true;')
    srv_control.run_command(step, 'ddns-update-style interim;')
    srv_control.run_command(step, 'zone six.example.com. {primary 175.16.1.1; }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # #
    # # Grab a lease
    # #
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'myhost.bubba.com')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_requests_option(step, '39')
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
                                             '3000::2')
    srv_msg.log_contains_line(step,
                              'DHCP',
                              None,
                              'DDNS_STATE_ADD_FW_NXDOMAIN 3000::2 for myhost.six.example.com')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.ddns
@pytest.mark.forward
def test_v6_dhcpd_keyword_ddns_forward_do_forward_updates_false(step):
    """new-v6.dhcpd.keyword.ddns.forward.do-forward-updates.false"""
    # #
    # # Testing: Checks that a forward add is not attempted if do-forward-updates
    # # is set to false.
    # #
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/32', '3000::2-3000::2')
    srv_control.run_command(step, 'ddns-updates true;')
    srv_control.run_command(step, 'ddns-domainname "six.example.com";')
    srv_control.run_command(step, 'ddns-update-style interim;')
    srv_control.run_command(step, 'do-forward-updates false;')
    srv_control.run_command(step, 'zone EXAMPLE.ORG. {primary 127.0.0.1;}')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # #
    # # Grab a lease
    # #
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'six.example.com')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
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
                                             '3000::2')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'DDNS_STATE_ADD_FW_NXDOMAIN 3000::2')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.ddns
@pytest.mark.forward
def test_v6_dhcpd_keyword_ddns_forward_no_client_fqdn(step):
    """new-v6.dhcpd.keyword.ddns.forward.no-client-fqdn"""
    # #
    # # Testing: Checks that forward ddns updates are not attempted when
    # # no client FQDN option is supplied.
    # #
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/32', '3000::2-3000::2')
    srv_control.run_command(step, 'ddns-updates true;')
    srv_control.run_command(step, 'ddns-domainname "six.example.com";')
    srv_control.run_command(step, 'ddns-update-style interim;')
    srv_control.run_command(step, 'do-forward-updates true;')
    srv_control.run_command(step, 'zone EXAMPLE.ORG. {primary 127.0.0.1;}')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # #
    # # Grab a lease
    # #
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

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
                                             '3000::2')
    srv_msg.log_contains_line(step, 'DHCP', 'NOT ', 'DDNS_STATE_ADD_FW_NXDOMAIN 3000::2')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.ddns
@pytest.mark.forward
def test_v6_dhcpd_keyword_ddns_forward_ddns_hostname(step):
    """new-v6.dhcpd.keyword.ddns.forward.ddns-hostname"""
    # #
    # # Testing: Checks that hostname used as the FQDN in the forward add
    # # can be specified using ddns-hostname.
    # #
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/32', '3000::2-3000::2')
    srv_control.run_command(step, 'ddns-updates true;')
    srv_control.run_command(step, 'ddns-domainname "six.example.com";')
    srv_control.run_command(step, 'ddns-hostname "cfg_host";')
    srv_control.run_command(step, 'ddns-update-style interim;')
    srv_control.run_command(step, 'zone six.example.com. {primary 175.16.1.1; }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # #
    # # Grab a lease
    # #
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'myhost.bubba.com')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
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
                                             '3000::2')
    srv_msg.log_contains_line(step,
                              'DHCP',
                              None,
                              'DDNS_STATE_ADD_FW_NXDOMAIN 3000::2 for cfg_host.six.example.com')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.ddns
@pytest.mark.forward
def test_v6_dhcpd_keyword_ddns_forward_ddns_ttl(step):
    """new-v6.dhcpd.keyword.ddns.forward.ddns-ttl"""
    # #
    # # Testing: Checks that TTL sent with the forward add can be specified
    # # using ddns-ttl.
    # #
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/32', '3000::2-3000::2')
    srv_control.run_command(step, 'ddns-updates true;')
    srv_control.run_command(step, 'ddns-domainname "six.example.com";')
    srv_control.run_command(step, 'ddns-ttl 7701;')
    srv_control.run_command(step, 'ddns-update-style interim;')
    srv_control.run_command(step, 'zone six.example.com. {primary 175.16.1.1; }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # #
    # # Grab a lease
    # #
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'myhost.bubba.com')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
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
                                             '3000::2')
    srv_msg.log_contains_line(step, 'DHCP', None, 'ttl: 7701')



