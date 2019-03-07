"""DHCPv6 vendor specific information"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import srv_control
import misc
import references


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.vendor
def test_v6_options_vendor_tftp_servers():
    #  Testing server ability to configure it with vendor-specific options
    #  and share it with user.
    #  In this case: for vendor id vendor-4491 set option tftp-servers with value: 2001:558::76
    #  Send vendor class and vendor specific information option (with option request).
    #  Vendor tests are beta version.
    #  with client via Advertise message.
    #  							 Client		Server
    #  vendor-class
    #  specific-info-req (32)	SOLICIT -->
    #  vendor-spec-info 				<--	ADVERTISE
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					vendor specific information (code 17) with suboption
    # 					TFTP Server address (code 32)
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_opt_space('vendor-4491', 'tftp-servers', '2001:558::76')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1', '32')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')

    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '17')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '32')

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.vendor
def test_v6_options_vendor_config_file():
    #  Testing server ability to configure it with vendor-specific options
    #  and share it with user.
    #  In this case: for vendor id vendor-4491 set option config-file with value normal_erouter_v6.cm.
    #  Send vendor class and vendor specific information option (with option request).
    #  Vendor tests are beta version.
    #  with client via Advertise message.
    #  							 Client		Server
    #  vendor-class
    #  specific-info-req (33)	SOLICIT -->
    #  vendor-spec-info 				<--	ADVERTISE
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					vendor specific information (code 17) with suboption
    # 					Configuration file name (code 33)
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_opt_space('vendor-4491', 'config-file', 'normal_erouter_v6.cm')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1', '33')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')

    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '17')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '33')

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.vendor
def test_v6_options_vendor_syslog_servers():
    #  Testing server ability to configure it with vendor-specific options
    #  and share it with user.
    #  In this case: for vendor id vendor-4491 set option syslog-servers with address 2001::101.
    #  Send vendor class and vendor specific information option (with option request).
    #  Vendor tests are beta version.
    #  with client via Advertise message.
    #  							 Client		Server
    #  vendor-class
    #  specific-info-req (34)	SOLICIT -->
    #  vendor-spec-info 				<--	ADVERTISE
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					vendor specific information (code 17) with suboption
    # 					sys log servers (code 34)
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_opt_space('vendor-4491', 'syslog-servers', '2001::101')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1', '34')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')

    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '17')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '34')

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.vendor
def test_v6_options_vendor_time_servers():
    #  Testing server ability to configure it with vendor-specific options
    #  and share it with user.
    #  In this case: for vendor id vendor-4491 set option time-servers option with value 2001::76.
    #  Send vendor class and vendor specific information option (with option request).
    #  Vendor tests are beta version.
    #  with client via Advertise message.
    #  							 Client		Server
    #  vendor-class
    #  specific-info-req (37)	SOLICIT -->
    #  vendor-spec-info 				<--	ADVERTISE
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					vendor specific information (code 17) with suboption
    # 					time protocol servers (code 37)

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_opt_space('vendor-4491', 'time-servers', '2001::76')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1', '37')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')

    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '17')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '37')

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.vendor
def test_v6_options_vendor_time_offset():
    #  Testing server ability to configure it with vendor-specific options
    #  and share it with user.
    #  In this case: for vendor id vendor-4491 set option time-offset with value -18000
    #  Send vendor class and vendor specific information option (with option request).
    #  Vendor tests are beta version.
    #  with client via Advertise message.
    #  							 Client		Server
    #  vendor-class
    #  specific-info-req (38)	SOLICIT -->
    #  vendor-spec-info 				<--	ADVERTISE
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					vendor specific information (code 17) with suboption
    # 					time offset (code 38)
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_opt_space('vendor-4491', 'time-offset', '-18000')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1', '38')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')

    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '17')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '38')

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.options
@pytest.mark.vendor
def test_v6_options_vendor_multiple():
    #  Testing server ability to configure it with vendor-specific options
    #  and share it with user.
    #  In this case: for vendor id vendor-4491 set option time-offset with value -18000
    #  and for vendor id vendor-4491 set option tftp-servers with value: 2001:558:ff18:16:10:253:175:76
    #  and for vendor id vendor-4491 set option config-file with value normal_erouter_v6.cm
    #  and for vendor id vendor-4491 set option syslog-servers with address 2001:558:ff18:10:10:253:124:101
    #  and for vendor id vendor-4491 set option time-servers option with value 2001:558:ff18:16:10:253:175:76
    #  and for vendor id vendor-4491 set option time-offset with value -10000
    #  Send vendor class and vendor specific information option (with option request).
    #  Vendor tests are beta version.
    #  with client via Advertise message.
    #  							 Client		Server
    #  vendor-class
    #  specific-info-req (all codes)SOLICIT -->
    #  vendor-spec-info 				<--	ADVERTISE
    #  Pass Criteria:
    #  				REPLY/ADVERTISE MUST include option:
    # 					vendor specific information (code 17) with suboption
    # 					TFTP Server address (code 32)
    # 					Configuration file name (code 33)
    # 					sys log servers (code 34)
    # 					time offset (code 38)
    # 					time protocol servers (code 37)

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/32', '3000::1-3000::2')
    srv_control.config_srv_opt_space('vendor-4491',
                                     'tftp-servers',
                                     '2001:558:ff18:16:10:253:175:76')
    srv_control.config_srv_opt_space('vendor-4491', 'config-file', 'normal_erouter_v6.cm')
    srv_control.config_srv_opt_space('vendor-4491',
                                     'syslog-servers',
                                     '2001:558:ff18:10:10:253:124:101')
    srv_control.config_srv_opt_space('vendor-4491',
                                     'time-servers',
                                     '2001:558:ff18:16:10:253:175:76')
    srv_control.config_srv_opt_space('vendor-4491', 'time-offset', '-10000')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', None, 'vendor-class')
    srv_msg.add_vendor_suboption('Client', '1', '32')
    srv_msg.add_vendor_suboption('Client', '1', '33')
    srv_msg.add_vendor_suboption('Client', '1', '34')
    srv_msg.add_vendor_suboption('Client', '1', '37')
    srv_msg.add_vendor_suboption('Client', '1', '38')
    srv_msg.client_does_include('Client', None, 'vendor-specific-info')

    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '17')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '32')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '33')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '34')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '37')
    srv_msg.response_check_option_content('Response', '17', None, 'sub-option', '38')

    references.references_check('RFC3315')
